from typer import Typer

# from evedata_platform_sources._old_sde import (
#     archive_current_sde_version,
#     current_archived_sde_version,
#     current_ccp_sde_version,
#     stage_archived_sde,
# )


cmd = Typer(name="sde")


@cmd.callback()
def callback():
    """Manage Static Data Export (SDE) archives."""


# @cmd.command(name="archive")
# def archive_cmd(
#     *,
#     ctx: typer.Context,
#     force: Annotated[bool, typer.Option(help="Overwrite existing archive")] = False,
# ) -> None:
#     """Archive the current SDE version."""
#     state: AdminState = ctx.obj
#     config = state.config
#     err = state.err

#     current_ccp_version = current_ccp_sde_version()
#     current_archive_version = current_archived_sde_version(config)

#     if current_ccp_version == current_archive_version and not force:
#         err.print(
#             f"SDE version {current_ccp_version} is already archived. "
#             "Use --force to re-archive."
#         )
#         raise typer.Exit(2)

#     archive_current_sde_version(config, overwrite=force)


# @cmd.command(name="stage")
# def stage_cmd(
#     *,
#     ctx: typer.Context,
#     output_dir: Annotated[
#         "Path | None",
#         typer.Option(
#             "--output",
#             "-o",
#             help="Directory to stage to",
#             dir_okay=True,
#             file_okay=False,
#             writable=True,
#             resolve_path=True,
#         ),
#     ] = None,
#     version: Annotated[
#         str | None,
#         typer.Option(help="SDE version to stage. Defaults to latest archived."),
#     ] = None,
#     force: Annotated[
#         bool, typer.Option(help="Overwrite existing staged version")
#     ] = False,
# ) -> None:
#     """Stage an archived SDE version by downloading and extracting it."""
#     state: AdminState = ctx.obj
#     config = state.config
#     err = state.err
#     out = state.out

#     if version is None:
#         version = current_archived_sde_version(config)
#         if version is None:
#             err.print("No archived SDE versions found.")
#             raise typer.Exit(1)

#     output_dir = output_dir or config.sde_staging_dir / version

#     out.print(f"Staging SDE version {version} to {output_dir}")
#     stage_archived_sde(config, output_dir, version, overwrite=force)
