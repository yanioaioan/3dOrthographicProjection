import maya.cmds as cmds

if cmds.objExists('FEMUR*'):
    cmds.select('FEMUR*')  
    cmds.delete()

    
    
cmds.file('/home/yioannidis/3dOrthographicProjection/vpilm07mcj-Femur/' + 'FEMUR-part.obj', i=True)

# http://www.fevrierdorian.com/blog/post/2011/09/27/Quickly-retrieve-vertex-positions-of-a-Maya-mesh-(English-Translation)
def getVtxPos( shapeNode ) :
 
     vtxWorldPosition = []    # will contain positions un space of all object vertex
 
     vtxIndexList = cmds.getAttr( shapeNode+".vrts", multiIndices=True )
 
     for i in vtxIndexList :
          curPointPosition = cmds.xform( str(shapeNode)+".pnts["+str(i)+"]", query=True, translation=True, worldSpace=True )    # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]
          vtxWorldPosition.append( curPointPosition )
 
     return vtxWorldPosition

if cmds.objExists('pCube1'):
  cmds.select('pCube1')
  cmds.delete()
else:
  print("Warning: no pCube1 exists.")

   
cube=cmds.polyCube()


femur=cmds.ls( 'FEMUR*' )
obj=femur

cubeVertices = getVtxPos(obj[0])

projectedPoints = []
cx, cz = 0,0
sx,sz = 1,1
for i in range(len(cubeVertices)):
        
    ax,ay,az =cubeVertices[i]
    
    
    bx = sx * ax + cx
    by = sz * az + cz
    
    projectedPoints.append((bx,by))
    
for i in range(1,len(projectedPoints)+1):
    if cmds.objExists('pSphere'+str(i)):
      cmds.select('pSphere'+str(i))
      cmds.delete()
     
#create silhouette 
for i in range(len(projectedPoints)):      
    cmds.polySphere()
    cmds.xform(translation=(projectedPoints[i][0],projectedPoints[i][1], -50), scale=(0.1,0.1,0.1) )

#show silhouette extraced in orthographic project


'''select and show projected points'''
#cmds.select('pSphere*')


'''MANUALY TRANSLATE projected points'''

#Now create a associative relationship/map between each 3D&2D point, so as when I apply a transformation to one the other is also affected

#find difference between previous projectedPoints and currentProjectedPoints
currentProjectedPoints=[]
for i in range(1,len(projectedPoints)+1):      
    #print cmds.xform('pSphere'+str(i), translation=True, query=True)
    currentProjectedPoints.append(cmds.xform('pSphere'+str(i), translation=True, query=True))

traslationUpdateVector = []    
for i in range(len(currentProjectedPoints)):
    if (currentProjectedPoints[i][0]-projectedPoints[i][0] , currentProjectedPoints[i][1]-projectedPoints[i][1]) != (0,0):
        print 'difference in translation between currentProjectedPoints and projectedPoints =', (currentProjectedPoints[i][0]-projectedPoints[i][0] , currentProjectedPoints[i][1]-projectedPoints[i][1])
    
    traslationUpdateVector.append( (currentProjectedPoints[i][0]-projectedPoints[i][0] , currentProjectedPoints[i][1]-projectedPoints[i][1]) )

print traslationUpdateVector

for vertexId in range(len(currentProjectedPoints)):
    cmds.select('FEMUR.vtx['+str(vertexId)+']')
    #print len(traslationUpdateVector)
    print vertexId
    print traslationUpdateVector[vertexId]
    cmds.xform(r=True, translation=(traslationUpdateVector[vertexId][0], traslationUpdateVector[vertexId][1], 0))
    
 