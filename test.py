import unittest
import tests.emoeaTests as emoea
import tests.costTests as cost
import mapping.network_mapping as nm
import elementtree. ElementTree as ET
#import tests.testInterface as interface
if __name__ == "__main__":
    #interface.main()
    #unittest.main(emoea)
    #unittest.main(cost)
    r = nm.Routes("/home/numix/school/ea/cs448/data/tapascologne-0.0.1/routes6-8.rou.xml")
    g = nm.Graph("/home/numix/school/ea/cs448/data/tapascologne-0.0.1/cologne.nod.xml", "/home/numix/school/ea/cs448/data/tapascologne-0.0.1/cologne.edg.xml", "data/rand/rand.flo.xml")
    g.load()
    g.trim(r, (18641, 19535), (33850, 35412))
    r.writexml()
    g.writexml()
