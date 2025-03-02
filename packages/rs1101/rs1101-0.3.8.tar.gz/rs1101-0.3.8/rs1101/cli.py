import rs1101.random_string as rs
import rs1101.random_format as rf
import click
import cloup


class Repo:
    pass


default_length = 10


@click.group(invoke_without_command=True)
@cloup.option_group(
    "candidate options",
    click.option(
        "-c",
        type=click.Choice(list(rs.candidate_dict.keys())),
        multiple=True,
        default=rs.cddt_default,
        help="candidate options",
    ),
    click.option("-cs", type=str, default="", help="candidata string"),
    constraint=cloup.constraints.mutually_exclusive,
)
@click.option("-l", help="the length of the generated string", type=int, default=None)
@click.option(
    "-s",
    type=str,
    default=None,
    help="secret string",
)
@click.option(
    "-ss",
    is_flag=True,
    show_default=True,
    default=False,
    help="show strength",
)
@click.pass_context
def cli(ctx, c, cs, l, ss, s):
    """
    \b
    candidate options:
        d: digits,  # 10
        h: hexdigits,  # 16
        H: Hexdigits,  # 16
        l: ascii_lowercase,  # 26
        u: ascii_uppercase,  # 26
        p: punctuation,  # 32
        i: ascii_letters + digits + punctuation,  # 26*2+10+32=94
        a: printable,  # 100

    \b
    example:
        rs
        rs -l 6
        rs -c h -c p -l 12
        rs -s "secret_string" -l 15
        rs tint o8ymjbmJCfyvC8o
        rs fint 299353548720746608360952808
    """

    candidate = rs.g_candidate(c)
    if cs:
        candidate = cs
    ctx.obj = Repo()
    ctx.obj.candidate = candidate
    ctx.obj.length = l if l else default_length
    ctx.obj.ss = ss
    if ctx.invoked_subcommand is None:
        if l is None:
            l = default_length
        if s is not None:
            result = rs.s2rs(s, l, candidate)
        else:
            result = rs.random_string(l, candidate)
        print(result)
        show_strength(ctx.obj)
    else:
        if l is not None:
            raise click.BadOptionUsage(
                message="You should not use the -l option here when using the subcommand."
            )


@cli.command("tint", help="covert a string to an integer")
@click.argument("s", type=str)
@click.pass_obj
def cli_rs2int(obj, s):
    x = rs.rs2int(s, candidate=obj.candidate)
    obj.length = len(s)
    print(x)
    show_strength(obj)


@cli.command("fint", help="covert a string from an integer")
@click.argument("x", type=int)
@click.option("-l", help="the length of the generated string", type=int, default=None)
@click.pass_obj
def cli_int2rs(obj, x, l):
    s = rs.int2rs(x, length=l, candidate=obj.candidate)
    obj.length = len(s)
    print(s)
    show_strength(obj)


# @cli.command("gen")
# @click.option(
#     "-l", metavar="the length of the generated string", type=int, default=default_length
# )
# @click.pass_obj
# def cli_rs(obj, l):
#     s = rs.random_string(l, candidate=obj.candidate)
#     obj.length = l
#     print(s)
#     show_strength(obj)


def show_strength(obj):
    if obj.ss:
        print(f"strength:{rs.strength(obj.length,len(obj.candidate))}")


if __name__ == "__main__":
    # print(candidate_help_string)
    cli()
