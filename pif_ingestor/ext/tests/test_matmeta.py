from pif_ingestor.ext.matmeta import *

from pypif.obj.common import *
from pypif.obj.system import System

def test_update_pif_append():
    pif1 = System(properties=[Property(name="foo", scalars=[Scalar(value="bar")])])
    pif2 = System(properties=[Property(name="spam", scalars=[Scalar(value="eggs")])])
    new  = update_pif(pif1, pif2)
    assert len(new.properties) == 2
    assert set(x.name for x in new.properties) == set(["foo", "spam"])


def test_update_pif_replace():
    pif1 = System(uid="0") 
    pif2 = System(uid="1")
    new  = update_pif(pif1, pif2)
    assert new.uid == "1"


def test_update_pif_set():
    pif1 = System(contacts=[Person(name=Name(given="Steve", family="Holt"), email="cool@yeah.com")])
    pif2 = System(properties=[Property(name="spam", scalars=[Scalar(value="eggs")])])
    new  = update_pif(pif1, pif2)
    assert new.contacts[0].name.given == "Steve"
    assert new.contacts[0].email == "cool@yeah.com"
    assert new.properties[0].scalars[0].value == "eggs" 
