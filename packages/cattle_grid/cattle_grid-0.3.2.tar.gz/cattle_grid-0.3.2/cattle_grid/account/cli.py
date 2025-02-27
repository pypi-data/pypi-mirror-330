import click
import asyncio
import logging


from cattle_grid.database import run_with_database
from .models import Account, ActorForAccount
from .account import (
    create_account,
    add_permission,
    list_permissions,
    remove_permission,
    delete_account,
    add_actor_to_group,
)

logger = logging.getLogger(__name__)


async def new_account(name: str, password: str, permission: list[str]):
    account = await create_account(name, password)
    if account is None:
        click.echo("Failed to create account")
        exit(1)

    for p in permission:
        await add_permission(account, p)


async def list_accounts(actors):
    accounts = await Account.all().prefetch_related("permissions", "actors")
    for account in accounts:
        print(f"{account.name}: ", ", ".join(list_permissions(account)))
        if actors:
            for actor in account.actors:
                print(f"  {actor.name}: {actor.actor}")


async def modify_permissions(
    name: str, add_permissions: list[str], remove_permissions: list[str]
):
    account = await Account.get_or_none(name=name)
    if account is None:
        print(f"Account {name} does not exist")
        exit(1)
    for p in add_permissions:
        await add_permission(account, p)
    for p in remove_permissions:
        await remove_permission(account, p)


async def modify_actor(actor: str, add_groups: list[str]):
    actor_for_account = await ActorForAccount.get_or_none(actor=actor)

    if actor_for_account is None:
        print(f"Actor {actor} does not exist")
        exit(1)

    for group_name in add_groups:
        await add_actor_to_group(actor_for_account, group_name)


def add_account_commands(main):
    @main.group()
    def account():
        """Used to manage accounts associated with cattle_grid"""

    @account.command()  # type: ignore
    @click.argument("name")
    @click.argument("password")
    @click.option(
        "--admin", is_flag=True, default=False, help="Set the admin permission"
    )
    @click.option(
        "--permission",
        help="Adds the permission to the account",
        multiple=True,
        default=[],
    )
    @click.pass_context
    def new(ctx, name, password, admin, permission):
        """Creates a new account"""

        if admin:
            permission = list(permission) + ["admin"]

        asyncio.run(
            run_with_database(
                ctx.obj["config"], new_account(name, password, permission)
            )
        )

    @account.command()  # type: ignore
    @click.argument("name")
    @click.option(
        "--add_permission",
        help="Adds the permission to the account",
        multiple=True,
        default=[],
    )
    @click.option(
        "--remove_permission",
        help="Adds the permission to the account",
        multiple=True,
        default=[],
    )
    @click.pass_context
    def modify(ctx, name, add_permission, remove_permission):
        """Modifies an account"""

        asyncio.run(
            run_with_database(
                ctx.obj["config"],
                modify_permissions(
                    name,
                    add_permissions=add_permission,
                    remove_permissions=remove_permission,
                ),
            )
        )

    @account.command("modify-actor")  # type: ignore
    @click.argument("actor")
    @click.option("--add_group", multiple=True, default=[])
    @click.pass_context
    def modify_actor_command(ctx, actor, add_group):
        """Adds a group to the actor"""
        asyncio.run(
            run_with_database(ctx.obj["config"], modify_actor(actor, add_group))
        )

    @account.command("list")  # type: ignore
    @click.option(
        "--actors",
        is_flag=True,
        default=False,
        help="If set, also lists the actors associated with each account",
    )
    @click.pass_context
    def list_account(ctx, actors):
        """Lists existing accounts"""
        asyncio.run(run_with_database(ctx.obj["config"], list_accounts(actors)))

    @account.command("delete")  # type: ignore
    @click.argument("name")
    @click.pass_context
    def delete_account_command(ctx, name):
        """Lists existing accounts"""
        asyncio.run(
            run_with_database(ctx.obj["config"], delete_account(name, force=True))
        )
