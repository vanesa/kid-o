import unittest
from app import app
from app.child import ChildView
from app.models import Child
from datetime import datetime

class ChildViewTestCase(unittest.TestCase):
    
    def test_child_view(self):
        first_name = "Martha"
        last_name = "Sosa"
        birth_date= datetime.strptime("2009-02-02", "%Y-%m-%d")

        child = Child(first_name=first_name, last_name=last_name, birth_date=birth_date)

        test_child_view = ChildView(child)

        self.assertEqual(test_child_view.age, 6)


if __name__ == "__main__":
    unittest.main()
