import click
from db import getDbAll,getDbByUser


@click.group()
def cli():
    pass

@cli.command()
@click.option("-name",default=None, help="默认查询所有组件，-name=name 可以查询指定名字的组件", type=str)
@click.option("-id",default=None, help="默认查询所有组件， -id=id 可以查询指定名字的组件", type=str)
@click.option("-user" ,default=None, help="默认查询用户的所有组件，-user=user可以查询指定用户的组件", type=str)
@click.option('-d','--detail',is_flag=True,help='展示组件信息细节')
def show(name,detail,user,id):
    '''
    查询算盘组件信息
    :return:
    '''
    detail_flag = False
    if detail:
        detail_flag = True
    if user:
        show_by_user(user,detail_flag)
        return
    if name:
        show_by_name(name,detail_flag)
        return
    if id:
        show_by_id(id,detail_flag)
        return
    else:
        show_all(detail_flag)


def show_by_user(user,detail_flag):
    if detail_flag:
        click.echo('正在查询算盘所有组件细节')
        click.echo('-'*50)
        click.echo('正在查询算盘所有组件细节')
    else:
        click.echo(getDbByUser(user))
        
def show_by_name(name,detail_flag):
    df =getDbAll()
    click.echo(df[df.name == name])
        
def show_by_id(id,detail_flag):
    df =getDbAll()
    click.echo(df[df.id == int(id)]) 


def show_all(detail_flag):
    if detail_flag:
        show_all_detail()
    else:
        show_all_outline()
        
        
def show_all_detail():
    click.echo('正在查询算盘所有组件细节')
    click.echo('-'*50)
    click.echo('正在查询算盘所有组件细节')
    
def show_all_outline():
    click.echo(getDbAll())

    

       
    
    
@cli.command()
def add():
    '''
    增加算盘组件
    :return:
    '''
    click.echo('正在增加算盘组件')

if __name__ == '__main__':
    cli()