#!/usr/bin/env python3

# Standard libraries
from collections import namedtuple
import contextlib
from os import remove
from os.path import join
from pathlib import Path
from shutil import make_archive, rmtree, unpack_archive
from tempfile import TemporaryDirectory
from time import sleep
from typing import Any, cast, Dict, List, Optional, Tuple, Union

# Modules libraries
from gitlab import Gitlab
from gitlab.exceptions import (
    GitlabDeleteError,
    GitlabGetError,
    GitlabHttpError,
    GitlabListError,
)
from gitlab.v4.objects import (
    Group,
    Namespace,
    Project,
    ProjectBranchManager,
    ProjectCommitManager,
    ProjectImport,
    ProjectLabelManager,
    ProjectMergeRequestManager,
    ProjectPackageManager,
    ProjectPipelineManager,
    ProjectSnippetManager,
    ProjectTagManager,
    User,
)

# Components
from ..prints.colors import Colors
from ..types.gitlab import MigrationEntities
from ..types.namespaces import Namespaces

# GitLabFeature class, pylint: disable=too-many-public-methods
class GitLabFeature:

    # Constants
    DIFFERENCES_UNAVAILABLE: str = 'Unavailable'
    LIMITATIONS_ERROR: str = 'limitations-error'
    LIMITATIONS_WARNING: str = 'limitations-warning'
    TIMEOUT_CREATION: int = 60
    TIMEOUT_EXPORT: int = 300
    TIMEOUT_DELETION: int = 300

    # Members
    __dry_run: bool = False
    __gitlab: Gitlab

    # Constructor, pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        url: str,
        private_token: str,
        job_token: str,
        ssl_verify: Union[bool, str] = True,
        dry_run: bool = False,
    ) -> None:

        # Initialize members
        self.__dry_run = dry_run

        # Create GitLab client
        if private_token:
            self.__gitlab = Gitlab(
                url=url,
                private_token=private_token,
                ssl_verify=ssl_verify,
            )
        elif job_token:
            self.__gitlab = Gitlab(
                url=url,
                job_token=job_token,
                ssl_verify=ssl_verify,
            )
        else:
            self.__gitlab = Gitlab(
                url=url,
                ssl_verify=ssl_verify,
            )

        # Authenticate if available
        if self.__gitlab.private_token or self.__gitlab.oauth_token:
            self.__gitlab.auth()

    # Group
    def group(
        self,
        criteria: str,
        optional: bool = False,
    ) -> Group:

        # Optional group for dry run
        if self.__dry_run and optional:
            try:
                return self.group(criteria, optional=False)

            # Simulate group
            except GitlabGetError:
                GroupTuple = namedtuple('GroupTuple', [
                    'id',
                    'name',
                    'full_path',
                    'projects',
                ])

                # pylint: disable=no-self-use,too-few-public-methods
                class GroupProjects:
                    def list(self, **_kwargs: Optional[Any]) -> List[str]:
                        return []

                # Create fake group
                _, path = Namespaces.split_namespace(
                    criteria,
                    relative=False,
                )
                return cast(
                    Group,
                    GroupTuple(
                        id='dry-run',
                        name=path,
                        full_path=criteria,
                        projects=GroupProjects(),
                    ),
                )

        # Get group
        return self.__gitlab.groups.get(criteria)

    # Group create
    def group_create(
        self,
        path: str,
        name: str,
    ) -> None:

        # Create group
        if not self.__dry_run:
            self.__gitlab.groups.create({
                'parent_id': None,
                'path': path,
                'name': name,
            })

            # Wait for creation
            for _ in range(GitLabFeature.TIMEOUT_CREATION):
                sleep(1)
                try:
                    self.group(path)
                    break
                except GitlabGetError:
                    continue

    # Group delete
    def group_delete(
        self,
        criteria: str,
    ) -> None:

        # Delete group
        if not self.__dry_run:
            group = self.group(criteria)
            group.delete()
            sleep(1)
            try:
                group = self.group(criteria)
                group.delete(query_data={
                    'full_path': group.full_path,
                    'permanently_remove': 'true',
                })
            except (GitlabDeleteError, GitlabGetError):
                pass

            # Wait for deletion
            for _ in range(GitLabFeature.TIMEOUT_DELETION):
                sleep(1)
                try:
                    group = self.group(criteria)
                    if group.marked_for_deletion_on:
                        break
                except AttributeError:
                    pass
                except GitlabGetError:
                    break

        # Delay for deletion
        sleep(3)

    # Group export
    def group_export(
        self,
        archive: str,
        criteria: str,
        reset_entities_string: str = '',
    ) -> None:

        # Validate group access
        if self.__dry_run:
            return

        # Create group export
        group = self.group(criteria)
        group_export = group.exports.create()
        sleep(5)

        # Download group export
        for _ in range(GitLabFeature.TIMEOUT_EXPORT):
            sleep(1)
            try:
                with open(archive, 'wb') as file:
                    group_export.download(streamed=True, action=file.write)
                    break
            except GitlabGetError:
                continue

        # Parse migration entities
        reset_entities: List[str] = GitLabFeature.migration_entities_parse(
            reset_entities_string)
        reset_entities_names: List[str] = [
            MigrationEntities.get(entity).name for entity in reset_entities
        ]
        print(f'{Colors.BOLD}     - Reset entities: '
              f'{Colors.CYAN}{", ".join(reset_entities_names)}'
              f'{Colors.RESET}')

        # Reset migration entities
        if reset_entities:
            with TemporaryDirectory() as temp_directory:
                stem = archive
                if stem.endswith('.tar.gz'):
                    stem = stem[:-len('.tar.gz')]
                unpack_archive(archive, temp_directory, 'gztar')
                for reset_entity in reset_entities:
                    entity = MigrationEntities.get(reset_entity)
                    for group_glob in entity.group_globs:
                        for path in Path(temp_directory).glob(group_glob):
                            with contextlib.suppress(FileNotFoundError):
                                path.unlink()
                remove(archive)
                make_archive(stem, 'gztar', temp_directory)

    # Group export limitations
    def group_export_limitations(
        self,
        criteria: str,
    ) -> Dict[str, Tuple[str, List[str]]]:

        # Variables
        result: Dict[str, Tuple[str, List[str]]] = {}

        # Get group
        group = self.group(criteria)

        # Limitations: CI variables
        try:
            if group.variables.list(get_all=False):
                result['Variables'] = (
                    GitLabFeature.LIMITATIONS_ERROR,
                    [variable.key for variable in group.variables.list(get_all=True)],
                )
        except GitlabListError:
            pass

        # Result
        return result

    # Group import, pylint: disable=too-many-arguments
    def group_import(
        self,
        archive: str,
        parent: str,
        path: str,
        name: str,
    ) -> None:

        # Validate group access
        if self.__dry_run:
            return

        # Upload group import
        with open(archive, 'rb') as file:
            self.__gitlab.groups.import_group(
                file,
                path=path,
                name=name,
                parent_id=self.group(parent).id if parent else None,
            )
            sleep(5)

    # Group reset members
    def group_reset_members(
        self,
        criteria: str,
    ) -> None:

        # Remove group members
        group = self.group(criteria)
        for member in group.members.list(get_all=True):
            if not self.__dry_run:
                group.members.delete(member.id)

        # Save group
        if not self.__dry_run:
            group.save()

    # Group set avatar
    def group_set_avatar(
        self,
        criteria: str,
        file: str,
    ) -> None:

        # Set group avatar
        if not self.__dry_run:
            group = self.group(criteria)
            with open(file, 'rb') as avatar:
                group.avatar = avatar

                # Save group
                group.save()

    # Group set description
    def group_set_description(
        self,
        criteria: str,
        description: str,
    ) -> bool:

        # Variables
        changed: bool = False

        # Set group description
        if not self.__dry_run:
            group = self.group(criteria)
            if group.description != description:
                group.description = description
                changed = True

                # Save group
                group.save()

        # Result
        return changed

    # Migration entities parser
    @staticmethod
    def migration_entities_parse(input_string: str) -> List[str]:

        # Handle empty input
        if not input_string:
            return []

        # Parse entities from input
        return [
            key # Key
            for search in input_string.split(',') # Input entities
            for key in MigrationEntities.keys() # GitLab entities
            if MigrationEntities.get(key).name.lower().startswith(search.strip().lower())
        ]

    # Migration projects comparator
    @staticmethod
    def migration_projects_compare(
        input_project: Project,
        output_project: Project,
    ) -> List[Tuple[str, str]]:

        # Variables
        result_input: str
        result_output: str
        differences: List[Tuple[str, str]] = []

        # Count project items
        def count_project_items(
            resource: Union[
                ProjectBranchManager,
                ProjectCommitManager,
                ProjectLabelManager,
                ProjectMergeRequestManager,
                ProjectPackageManager,
                ProjectPipelineManager,
                ProjectSnippetManager,
                ProjectTagManager,
            ],
            flag_all: bool = False,
        ) -> str:
            if not resource:
                return '0'
            try:
                if flag_all:
                    return str(len(resource.list(get_all=True, all=True)))
                return str(len(resource.list(get_all=True)))
            except GitlabListError:
                return GitLabFeature.DIFFERENCES_UNAVAILABLE

        # Validate branches count
        result_input = count_project_items(input_project.branches)
        result_output = count_project_items(output_project.branches)
        if result_input != result_output:
            differences += [(
                'Branches count',
                f'{result_input} branches in input project, '
                f'{result_output} in output project',
            )]

        # Validate commits count
        result_input = count_project_items(input_project.commits, flag_all=True)
        result_output = count_project_items(output_project.commits, flag_all=True)
        if result_input != result_output:
            differences += [(
                'Commits count',
                f'{result_input} commits in input project, '
                f'{result_output} in output project',
            )]

        # Validate tags count
        result_input = count_project_items(input_project.tags)
        result_output = count_project_items(output_project.tags)
        if result_input != result_output:
            differences += [(
                'Tags count',
                f'{result_input} tags in input project, '
                f'{result_output} in output project',
            )]

        # Validate merge requests count
        result_input = count_project_items(input_project.mergerequests)
        result_output = count_project_items(output_project.mergerequests)
        if result_input != result_output:
            differences += [(
                'Merge requests count',
                f'{result_input} merge requests in input project, '
                f'{result_output} in output project',
            )]

        # Validate labels count
        result_input = count_project_items(input_project.labels)
        result_output = count_project_items(output_project.labels)
        if result_input != result_output:
            differences += [(
                'Labels count',
                f'{result_input} labels in input project, '
                f'{result_output} in output project',
            )]

        # Validate pipelines count
        result_input = count_project_items(input_project.pipelines)
        result_output = count_project_items(output_project.pipelines)
        if result_input not in [result_output, GitLabFeature.DIFFERENCES_UNAVAILABLE]:
            differences += [(
                'Pipelines count',
                f'{result_input} pipelines in input project, '
                f'{result_output} in output project',
            )]

        # Validate packages count
        result_input = count_project_items(input_project.packages)
        result_output = count_project_items(output_project.packages)
        if result_input not in [result_output, GitLabFeature.DIFFERENCES_UNAVAILABLE]:
            differences += [(
                'Pipelines count',
                f'{result_input} packages in input project, '
                f'{result_output} in output project',
            )]

        # Validate snippets count
        result_input = count_project_items(input_project.snippets)
        result_output = count_project_items(output_project.snippets)
        if result_input not in [result_output, GitLabFeature.DIFFERENCES_UNAVAILABLE]:
            differences += [(
                'Snippets count',
                f'{result_input} snippets in input project, '
                f'{result_output} in output project',
            )]

        # Result
        return differences

    # Namespace
    def namespace(self, criteria: str, optional: bool = False) -> Namespace:

        # Optional namespace for dry run
        if self.__dry_run and optional:
            try:
                return self.namespace(criteria, optional=False)

            # Simulate namespace
            except GitlabGetError:
                NamespaceTuple = namedtuple('NamespaceTuple', [
                    'id',
                    'name',
                    'full_path',
                    'kind',
                ])

                # Create fake namespace
                _, path = Namespaces.split_namespace(
                    criteria,
                    relative=False,
                )
                return cast(
                    Namespace,
                    NamespaceTuple(
                        id='dry-run',
                        name=path,
                        full_path=criteria,
                        kind='group',
                    ),
                )

        # Get namespace
        return self.__gitlab.namespaces.get(criteria)

    # Namespace projects
    def namespace_projects(
        self,
        criteria: str,
    ) -> Any:

        # Acquire namespace
        namespace = self.namespace(criteria, optional=self.__dry_run)

        # Get user projects
        if namespace.kind == 'user':
            user = self.user(criteria)
            return user.projects.list(get_all=True)

        # Get group projects
        return self.group(criteria, optional=self.__dry_run).projects.list(
            get_all=True,
            include_subgroups=True,
        )

    # Project
    def project(
        self,
        criteria: str,
    ) -> Project:
        return self.__gitlab.projects.get(criteria)

    # Project delete
    def project_delete(
        self,
        criteria: str,
    ) -> None:

        # Delete project
        if not self.__dry_run:
            try:
                project = self.project(criteria)
                project.delete()
                sleep(1)
                try:
                    project = self.project(criteria)
                    project.delete(
                        query_data={
                            'full_path': project.path_with_namespace,
                            'permanently_remove': 'true',
                        })
                except (GitlabDeleteError, GitlabGetError):
                    pass

            # Ignore missing project
            except GitlabGetError:
                pass

            # Wait for deletion
            for _ in range(GitLabFeature.TIMEOUT_DELETION):
                sleep(1)
                try:
                    project = self.project(criteria)
                    if project.marked_for_deletion_on:
                        break
                except AttributeError:
                    pass
                except GitlabGetError:
                    break

        # Delay for deletion
        sleep(3)

    # Project export
    def project_export(
        self,
        archive: str,
        criteria: str,
        reset_entities_string: str = '',
    ) -> None:

        # Validate project access
        if self.__dry_run:
            return

        # Create project export
        project = self.project(criteria)
        project_export = project.exports.create()
        project_export.refresh()
        while project_export.export_status not in ['finished', 'failed']:
            sleep(1)
            project_export.refresh()

        # Failed project export
        if project_export.export_status == 'failed':
            raise RuntimeError(project_export)

        # Download project export
        with open(archive, 'wb') as file:
            project_export.download(streamed=True, action=file.write)

        # Parse migration entities
        reset_entities: List[str] = GitLabFeature.migration_entities_parse(
            reset_entities_string)
        reset_entities_names: List[str] = [
            MigrationEntities.get(entity).name for entity in reset_entities
        ]
        print(f'{Colors.BOLD}     - Reset entities: '
              f'{Colors.CYAN}{", ".join(reset_entities_names)}'
              f'{Colors.RESET}')

        # Reset migration entities
        if reset_entities:
            with TemporaryDirectory() as temp_directory:
                stem = archive
                if stem.endswith('.tar.gz'):
                    stem = stem[:-len('.tar.gz')]
                unpack_archive(archive, temp_directory, 'gztar')
                for reset_entity in reset_entities:
                    entity = MigrationEntities.get(reset_entity)
                    for project_directory in entity.project_directories:
                        with contextlib.suppress(FileNotFoundError):
                            rmtree(Path(join(temp_directory, project_directory)),
                                   ignore_errors=True)
                    for project_file in entity.project_files:
                        with contextlib.suppress(FileNotFoundError):
                            Path(join(temp_directory, project_file)).unlink()
                remove(archive)
                make_archive(stem, 'gztar', temp_directory)

    # Project export limitations
    def project_export_limitations(
        self,
        criteria: str,
    ) -> Dict[str, Tuple[str, List[str]]]:

        # Variables
        result: Dict[str, Tuple[str, List[str]]] = {}

        # Get project
        project = self.project(criteria)

        # Limitations: Packages registry
        try:
            if project.packages.list(get_all=False):
                result['Packages registry'] = (
                    GitLabFeature.LIMITATIONS_WARNING,
                    [
                        f'{package.name}:{package.version}'
                        for package in project.packages.list(get_all=True)
                    ],
                )
        except GitlabListError:
            pass

        # Limitations: Container registry
        try:
            if project.repositories.list(get_all=False):
                result['Container registry'] = (
                    GitLabFeature.LIMITATIONS_ERROR,
                    [
                        f'{container.location}:{container.name if container.name else "latest"}'
                        for container in project.repositories.list(get_all=True)
                    ],
                )
        except GitlabListError:
            pass

        # Limitations: CI variables
        try:
            if project.variables.list(get_all=False):
                result['Variables'] = (
                    GitLabFeature.LIMITATIONS_ERROR,
                    [variable.key for variable in project.variables.list(get_all=True)],
                )
        except GitlabListError:
            pass

        # Limitations: Pipeline triggers
        try:
            if project.triggers.list(get_all=False):
                result['Pipeline triggers'] = (
                    GitLabFeature.LIMITATIONS_ERROR,
                    [
                        trigger.description
                        for trigger in project.triggers.list(get_all=True)
                    ],
                )
        except GitlabListError:
            pass

        # Limitations: Webhooks
        try:
            if self.__gitlab.http_get(f'/projects/{project.id}/hooks', get_all=True):
                result['Webhooks'] = (
                    GitLabFeature.LIMITATIONS_ERROR,
                    [
                        hook.get('name', hook['url']) # type: ignore[index,union-attr]
                        for hook in self.__gitlab.http_get(
                            f'/projects/{project.id}/hooks', get_all=True)
                    ],
                )
        except GitlabHttpError:
            pass

        # Limitations: Project Access Tokens
        try:
            if project.access_tokens.list(get_all=False):
                result['Project Access Tokens'] = (
                    GitLabFeature.LIMITATIONS_ERROR,
                    [token.name for token in project.access_tokens.list(get_all=True)],
                )
        except GitlabListError:
            pass

        # Result
        return result

    # Project get branch default
    def project_get_branch_default(
        self,
        criteria: str,
    ) -> str:

        # Get default branch
        project = self.project(criteria)
        try:
            if project.default_branch:
                return str(project.default_branch)
        except AttributeError:
            pass

        # Result
        return ''

    # Project import, pylint: disable=too-many-arguments,too-many-positional-arguments
    def project_import(
        self,
        archive: str,
        group: str,
        path: str,
        name: str,
        overwrite: bool = False,
        sudo: Optional[str] = None,
    ) -> ProjectImport:

        # Validate project access
        if self.__dry_run:
            ProjectTuple = namedtuple('ProjectTuple', [
                'id',
                'name',
                'description',
                'path_with_namespace',
            ])
            return cast(
                ProjectImport,
                ProjectTuple(
                    id='dry-run',
                    name=name,
                    description=Namespaces.capitalize(
                        name,
                        words=True,
                    ),
                    path_with_namespace=path,
                ),
            )

        # Upload project import
        with open(archive, 'rb') as file:
            project_imported = self.__gitlab.projects.import_project(
                file,
                path=path,
                name=name,
                namespace=group,
                overwrite=overwrite,
                sudo=sudo,
            )

        # Wait project import
        project_import = self.__gitlab.projects.get(
            project_imported['id'],
            lazy=True,
        ).imports.get()
        while project_import.import_status not in ['finished', 'failed']:
            sleep(1)
            project_import.refresh()

        # Handle failed import
        if project_import.import_status == 'failed':
            if not project_import.failed_relations \
                    and 'key not found: nil' in project_import.import_error:
                print(f'{Colors.BOLD}     - Legacy GitLab export/import error ignored: '
                      f'{Colors.RED}{project_import.import_error}'
                      f'{Colors.RESET}')
            else:
                raise RuntimeError(project_import.import_error)

        # Result
        return project_import

    # Project reset members
    def project_reset_members(
        self,
        criteria: str,
    ) -> None:

        # Remove project members
        if not self.__dry_run:
            project = self.project(criteria)
            for member in project.members.list(get_all=True):
                try:
                    project.members.delete(member.id)
                except GitlabDeleteError:
                    pass

            # Save project
            project.save()

    # Project set archive
    def project_set_archive(
        self,
        criteria: str,
        enabled: bool,
    ) -> bool:

        # Variables
        changed: bool = False

        # Archive project
        if not self.__dry_run and enabled:
            project = self.project(criteria)
            if not project.archived:
                project.archive()
                changed = True

        # Unarchive project
        elif not self.__dry_run:
            project = self.project(criteria)
            if project.archived:
                project.unarchive()
                changed = True

        # Result
        return changed

    # Project set avatar
    def project_set_avatar(
        self,
        criteria: str,
        file: str,
    ) -> None:

        # Set project avatar
        if not self.__dry_run:
            project = self.project(criteria)
            with open(file, 'rb') as avatar:
                project.avatar = avatar

                # Save project
                project.save()

    # Project set branch default
    def project_set_branch_default(
        self,
        criteria: str,
        default_branch: str,
    ) -> bool:

        # Variables
        changed: bool = False

        # Set default branch
        if not self.__dry_run:
            project = self.project(criteria)
            try:
                if project.default_branch and project.default_branch != default_branch:
                    project.default_branch = default_branch
                    changed = True
            except AttributeError:
                return changed

            # Save project
            if changed:
                project.save()

        # Result
        return changed

    # Project set description
    def project_set_description(
        self,
        criteria: str,
        description: str,
    ) -> bool:

        # Variables
        changed: bool = False

        # Set project description
        if not self.__dry_run:
            project = self.project(criteria)
            if project.description != description:
                project.description = description
                changed = True

                # Save project
                project.save()

        # Result
        return changed

    # Subgroup create
    def subgroup_create(
        self,
        parent: str,
        path: str,
        name: str,
    ) -> None:

        # Create subgroup
        if not self.__dry_run:
            group = self.group(parent)
            self.__gitlab.groups.create({
                'parent_id': group.id,
                'path': path,
                'name': name,
            })

            # Wait for creation
            for _ in range(GitLabFeature.TIMEOUT_CREATION):
                sleep(1)
                try:
                    self.group(path)
                    break
                except GitlabGetError:
                    continue

    # URL
    @property
    def url(self) -> str:
        return str(self.__gitlab.api_url)

    # User
    def user(
        self,
        criteria: str,
    ) -> User:
        users = self.__gitlab.users.list(all=True, iterator=True, username=criteria)
        for user in users:
            return cast(User, user)
        raise RuntimeError(f'Could not find user {criteria}')

    # User name
    @property
    def username(self) -> str:
        if self.__gitlab.user:
            return str(self.__gitlab.user.username)
        return '/'
