import unittest
from permissible.perm_def import PermDef
from permissible.perm_def.short_perms import ShortPermsMixin

# Pseudocode:
# 1. Create dummy classes for testing:
#    - DummyUser: has an id attribute and a has_perms method that returns a preset value.
#    - DummyObj: simulates a ShortPermsMixin object:
#         * Has _meta attribute with app_label and model_name.
#         * Has a pk attribute.
#         * Implements get_permission_codenames method.
#    - DummyRootObj: similar to DummyObj.
#    - DummyWithGetterStr: Implements a method "get_root" which returns a DummyObj.
#
# 2. Write test cases:
#    - test_check_global_success: Create a PermDef with short_perm_codes=None and condition_checker that always returns True.
#         Call check_global, expect True.
#    - test_check_global_fail_condition: PermDef with condition_checker that always returns False; check_global should not return True.
#    - test_check_obj_success: Use a PermDef with short_perm_codes not None and condition_checker True.
#         Create a dummy object with a valid pk. DummyUser.has_perms returns True. Expect check_obj returns True.
#    - test_check_obj_fail_nopk: Create a DummyObj with pk set to None and check_obj is expected to return False.
#    - test_obj_getter_function: Use obj_getter as a lambda that returns a modified object (DummyRootObj).
#         Expect check_obj returns True if root object has a valid pk.
#    - test_obj_getter_string: Use obj_getter as a string representing a method name on the object.
#         Create a dummy object with method get_root that returns a valid DummyObj. Expect check_obj returns True.
#
# 3. Import the PermDef and related constants with absolute import.
#


# Dummy user class
class DummyUser:
    def __init__(self, id, perms_result=True, pk=1):
        self.id = id
        self.perms_result = perms_result
        self.pk = pk

    def has_perms(self, perms, obj):
        return self.perms_result


# Dummy object simulating ShortPermsMixin
class DummyObj(ShortPermsMixin):
    _meta = type("Meta", (), {"app_label": "testapp", "model_name": "dummy"})

    def __init__(self, pk, allowed=True):
        self.pk = pk
        self.allowed = allowed

    # Example method for string-based condition checking
    def can_do(self, user, context):
        return True


# Dummy object to be returned by a getter function
class DummyRootObj(DummyObj):
    pass


# Dummy object with a method getter for string-based obj_getter
class DummyWithGetterStr(DummyObj):
    def __init__(self, root_obj):
        self.root_obj = root_obj
        self.pk = 999  # dummy pk for the parent, not used

    def get_root(self, context):
        return self.root_obj


class TestPermDef(unittest.TestCase):

    def test_check_global_success(self):
        # PermDef with empty short_perm_codes and condition_checker always True.
        perm_def = PermDef(short_perm_codes=[], condition_checker=lambda o, u, c: True)
        user = DummyUser(id=1)
        # Updated: pass DummyObj as the obj_class.
        self.assertTrue(
            perm_def.check_global(DummyObj, user, context={"extra": "value"})
        )

    def test_check_global_fail(self):
        # PermDef with null short_perm_codes and condition_checker always True.
        perm_def = PermDef(
            short_perm_codes=None, condition_checker=lambda o, u, c: True
        )
        user = DummyUser(id=1)
        # Updated: pass DummyObj as the obj_class.
        self.assertFalse(
            perm_def.check_global(DummyObj, user, context={"extra": "value"})
        )

    def test_check_global_fail_condition(self):
        # PermDef with a condition_checker that always returns False.
        perm_def = PermDef(
            short_perm_codes=None, condition_checker=lambda o, u, c: False
        )
        user = DummyUser(id=1)
        # Expect False when condition fails.
        self.assertFalse(perm_def.check_global(DummyObj, user))

    def test_check_global_no_condition(self):
        # When no condition_checker is provided, check_condition defaults to True.
        perm_def = PermDef(short_perm_codes=[])
        user = DummyUser(id=1)
        self.assertTrue(perm_def.check_global(DummyObj, user))

    def test_check_obj_success(self):
        # PermDef with a non-None short_perm_codes and condition_checker always True.
        perm_def = PermDef(
            short_perm_codes=["view"], condition_checker=lambda o, u, c: True
        )
        dummy_obj = DummyObj(pk=123)
        user = DummyUser(id=1, perms_result=True)
        self.assertTrue(perm_def.check_obj(dummy_obj, user))

    def test_check_obj_fail_nopk(self):
        # When object has no pk, check_obj should return False.
        perm_def = PermDef(
            short_perm_codes=["view"], condition_checker=lambda o, u, c: True
        )
        # Dummy object with pk set to None denotes missing pk.
        dummy_obj = DummyObj(pk=None)
        user = DummyUser(id=1, perms_result=True)
        self.assertFalse(perm_def.check_obj(dummy_obj, user))

    def test_obj_getter_function(self):
        # Use a lambda as obj_getter that returns a DummyRootObj with a valid pk.
        perm_def = PermDef(
            short_perm_codes=["view"],
            obj_getter=lambda obj, context: DummyRootObj(pk=555),
            condition_checker=lambda o, u, c: True,
        )
        dummy_obj = DummyObj(
            pk=1000
        )  # original object; will be transformed by obj_getter.
        user = DummyUser(id=1, perms_result=True)
        self.assertTrue(perm_def.check_obj(dummy_obj, user))

    def test_obj_getter_string(self):
        # Use a string as obj_getter, so that the object's method is used.
        perm_def = PermDef(
            short_perm_codes=["view"],
            obj_getter="get_root",
            condition_checker=lambda o, u, c: True,
        )
        root_obj = DummyObj(pk=777)
        dummy_with_getter = DummyWithGetterStr(root_obj=root_obj)
        user = DummyUser(id=1, perms_result=True)
        self.assertTrue(perm_def.check_obj(dummy_with_getter, user))

    def test_condition_checker_string(self):
        # Use a string as condition_checker to invoke an object's method.
        perm_def = PermDef(short_perm_codes=["view"], condition_checker="can_do")
        dummy_obj = DummyObj(pk=321)
        user = DummyUser(id=1, perms_result=True)
        self.assertTrue(perm_def.check_obj(dummy_obj, user))


if __name__ == "__main__":
    unittest.main()
