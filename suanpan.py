import imp
import click
from db import getDbAll,getDbByUser,getDetailById,getInfoById,getInfoByName,getPackages
import pandas as pd

EXPORT_PATH='C:/Users/wudai.xhw/Desktop/命令行工具/'

@click.group()
def cli():
    pass

@cli.command()
@click.option("-name",default=None, help="默认查询所有组件，-name=name 可以查询指定名字的组件", type=str)
@click.option("-id",default=None, help="默认查询所有组件， -id=id 可以查询指定名字的组件", type=int)
@click.option("-user" ,default=None, help="默认查询用户的所有组件，-user=user可以查询指定用户的组件", type=str)
# @click.option('-d','--detail',is_flag=True,help='展示组件信息细节')
def show(name,user,id):
    '''
    查询算盘组件信息
    :return:
    '''
    # detail_flag = False
    # if detail:
    #     detail_flag = True
    if user:
        show_by_user(user)
        return
    if name:
        show_by_name(name)
        return
    if id:
        show_by_id(id)
        return
    else:
        show_all()


def show_by_user(user):
    click.echo(getDbByUser(user))
        
def show_by_name(name):
    _id,_name,user_id,res =getInfoByName(name)
    if(_id):
        click.echo(res) 
        click.echo('-'*80)
        click.echo(getDetailById(id=_id,user_name=user_id))
    else:
        click.secho('-----------这个用户不存在-----------', fg='red')
        
def show_by_id(id):
    _id,name,user_id,res =getInfoById(id)
    if(_id):
        click.echo(res) 
        click.echo('-'*80)
        click.echo(getDetailById(id=id,user_name=user_id))
    else:
        click.secho('-----------这个id不存在-----------', fg='red')

def show_all():   
    show_all_outline()       
        
    
def show_all_outline():
    click.echo(getDbAll())

    
  
    
@cli.command()
@click.option("-addr",default=None, help="指定导入的文件夹地址", type=str,prompt='Your address please')
def import_comp():
    '''
    导入算盘组件
    :return:
    '''
    click.echo('正在导入算盘组件')


@cli.command()
@click.option("-addr",default=EXPORT_PATH, help="指定导出的文件夹地址", type=str,prompt='Your address please')
@click.option("-id",default=None, help="指定导出的组件id", type=int,prompt='id please')
def export_comp(addr,id):
    '''
    导出算盘组件
    :return:
    '''
    _id,_name,user_id,res =getInfoById(id)
    mes = getPackages(id=_id,user_name=user_id,to_path=addr)
    click.echo('正在导出算盘组件')
    click.echo(mes)
    
if __name__ == '__main__':
    cli()