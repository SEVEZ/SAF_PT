import maya.cmds as cmds
def PlacementTool():
	cmds.undoInfo(openChunk=True)
	Start = True
	if cmds.objExists('__Placement_Tool__'): 
		cmds.makeLive(none=True)
		if cmds.objExists('__Placement_Tool_c__'): cmds.delete('__Placement_Tool_c__')
		if cmds.objExists('__Placement_Tool_f__'): cmds.delete('__Placement_Tool_f__')
		if cmds.objExists('__Placement_Tool_g__'): cmds.delete('__Placement_Tool_g__')
		if cmds.objExists('__Placement_Tool__'): cmds.delete('__Placement_Tool__')
		cmds.xform(rp=(osPivot[0],osPivot[1],osPivot[2]),os=1)
		Start = False
		PT_START_UI()
	if Start:
		global osPivot
		osPivot=cmds.xform(q=1,rp=1,os=1)
		global wsPivot
		wsPivot=cmds.xform(q=1,rp=1,ws=1)
		cmds.setToolTo('moveSuperContext')
		sel=cmds.ls(sl=1,l=1)
		cmds.InvertSelection()
		cmds.select(cmds.ls(sl=1,v=1))
		cmds.select(cmds.filterExpand(sm=12))
		selAll=cmds.ls(sl=1)
		cmds.duplicate()
		cmds.group(name=('__Placement_Tool_g__'))
		cmds.CombinePolygons()
		cmds.hyperShade(assign='lambert1')
		cmds.polyMapDel()
		cmds.DeleteHistory()
		cmds.rename('__Placement_Tool__')
		cmds.hide()
		# Move Pivot
		cmds.select(sel)
		for i in sel :
		    pos = cmds.xform(i,q=1,ws=1,piv=1)
		    dup = cmds.duplicate(i,rr=1,po=1)
		    for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz'] :
		        if cmds.getAttr(dup[0]+'.'+attr,lock=True):cmds.setAttr(dup[0]+'.'+attr,lock=False)
		    shapeNode = cmds.ls(cmds.listRelatives(i,c=1,f=1),l=1,s=1)
		    for s in shapeNode :
		        cmds.parent(s,dup[0],add=1,s=1)
		    if cmds.listRelatives(dup[0],p=1) :
		        cmds.parent(dup[0],w=1)
		    cmds.setAttr(dup[0]+'.r',0,0,0,type="double3")              
		    bb=cmds.xform(dup[0],q=1,bb=1,ws=1)
		    cp=cmds.objectCenter(dup[0])
		    xpos=cp[0];ypos=bb[1];zpos = cp[2]
		    loc=cmds.spaceLocator()
		    cmds.xform(loc[0],ws=1,t=(xpos,ypos,zpos))
		    cmds.parent(loc[0],dup[0])
		    cmds.delete(cmds.parentConstraint(i,dup[0]))
		    pivPos=cmds.xform(loc[0],q=1,ws=1,t=1)
		    cmds.xform(i,ws=1,piv=(pivPos[0],pivPos[1],pivPos[2]))
		    cmds.delete(dup[0],loc[0])
		cmds.select(sel,r=1)
		cmds.select('__Placement_Tool__',r=1);cmds.select(sel,add=1)
		cmds.normalConstraint(worldUpType="none",aimVector=(0, 1, 0),upVector=(0, 1, 0),weight=1,name='__Placement_Tool_c__')
		cmds.select('__Placement_Tool__',r=1);cmds.makeLive()
		cmds.select(selAll)
		cmds.createDisplayLayer(name="__Placement_Tool_f__",number=1,nr=1)
		import maya.mel as mel
		mel.eval('layerEditorLayerButtonTypeChange("__Placement_Tool_f__")')
		mel.eval('layerEditorLayerButtonTypeChange("__Placement_Tool_f__")')
		cmds.select(sel)
		PT_STOP_UI()
	cmds.undoInfo(closeChunk=True)
def PT_START_UI():
	if (cmds.window('PT', exists=True)):
	        cmds.deleteUI('PT')
	cmds.window('PT',t=" ",s=0,tlb=1)
	cmds.columnLayout()
	cmds.button(l='Placement Tool\nSTART',c='PlacementTool()',bgc=(0.129,0.420,0.302),w=100,h=40)
	cmds.setParent()
	cmds.showWindow('PT')
def PT_STOP_UI():
	cmds.deleteUI('PT')
	cmds.window('PT',t=" ",s=0,tlb=1)
	cmds.columnLayout()
	cmds.button(l='Placement Tool\nSTOP',c='PlacementTool()',bgc=(1,0.420,0.302),w=100,h=40)
	cmds.setParent()
	cmds.showWindow('PT')
osPivot=[0.0,0.0,0.0]
wsPivot=[0.0,0.0,0.0]
PT_START_UI()
#import SAF_PT