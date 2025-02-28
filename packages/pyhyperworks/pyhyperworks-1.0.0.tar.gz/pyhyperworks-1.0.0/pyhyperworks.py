#------------------------------------------------------------------------------------------------#
# FILE    : PYHYPERWORKS CONFIG MAIN FILE
# VERSION : 1.0
# USAGE   : CONFIG PYHYPERWORKS TOOLS
# NOTICE  : ANY QUESTION, PLEASE CONTACT WITH zxx4477@126.com
#------------------------------------------------------------------------------------------------#

# imports
import os
import sys
import time
import hw # 将允许您访问框架类和函数。
import hm # 将允许您访问HyperMesh客户端类和函数。
import hm.entities # 将允许您访问HyperMesh客户端实体类。
import hw.hv #将导入HyperView类。
import hw.hg #将导入HyperGraph类。
import hw.taskmanager #将导入Task Manager类。
import hwx.gui #将导入GUI Toolkit类。

# constants
pyhw_home = os.path.dirname(os.path.abspath(__file__));

# check permission
sys.path.append(os.path.join(pyhw_home,'_pkgconfig'));
#import teamconfig
import pkgconfig