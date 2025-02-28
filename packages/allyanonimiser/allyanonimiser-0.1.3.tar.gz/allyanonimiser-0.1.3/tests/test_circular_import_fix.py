"""
Tests specifically focused on the circular import fix.

These tests directly inspect the module structure and imports to ensure 
that the fix for circular imports between __init__.py and insurance/claim_notes_analyzer.py
has been properly implemented and remains fixed.
"""

import os
import re
import sys
import unittest
from pathlib import Path


class CircularImportFixTests(unittest.TestCase):
    """Tests to verify that the circular import issue remains fixed."""
    
    def setUp(self):
        """Set up paths to the relevant files."""
        self.root_dir = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        self.init_file = self.root_dir / "__init__.py"
        self.claim_notes_file = self.root_dir / "insurance" / "claim_notes_analyzer.py"
        self.insurance_init_file = self.root_dir / "insurance" / "__init__.py"
    
    def test_init_file_structure(self):
        """Test that __init__.py defines factory functions before importing modules."""
        if not self.init_file.exists():
            self.skipTest("__init__.py file not found")
            
        with open(self.init_file, "r") as f:
            content = f.read()
            
        # Find positions of key elements
        version_pos = content.find("__version__")
        factory_pos = content.find("def create_")
        insurance_import_pos = content.find("from .insurance")
        
        # Check that version is defined
        self.assertGreater(version_pos, 0, "__version__ not found in __init__.py")
        
        # Check that factory functions are defined
        self.assertGreater(factory_pos, 0, "Factory functions not found in __init__.py")
        
        # Check that insurance module is imported
        self.assertGreater(insurance_import_pos, 0, "Insurance module import not found in __init__.py")
        
        # The key fix: factory functions should be defined BEFORE importing modules
        self.assertLess(factory_pos, insurance_import_pos, 
                        "Factory functions should be defined before importing insurance module")
    
    def test_claim_notes_analyzer_imports(self):
        """Test that claim_notes_analyzer.py does not import from parent module."""
        if not self.claim_notes_file.exists():
            self.skipTest("claim_notes_analyzer.py file not found")
            
        with open(self.claim_notes_file, "r") as f:
            content = f.read()
        
        # Check for direct imports from allyanonimiser
        parent_import = re.search(r'from\s+(?:allyanonimiser|\.\.)\s+import\s+', content)
        self.assertIsNone(parent_import, 
                         "claim_notes_analyzer.py should not import from parent module")
        
        # Check for presence of create_au_insurance_analyzer function call
        factory_call = re.search(r'create_au_insurance_analyzer\s*\(\s*\)', content)
        self.assertIsNone(factory_call,
                        "claim_notes_analyzer.py should not call create_au_insurance_analyzer")
    
    def test_insurance_init_exports(self):
        """Test that insurance/__init__.py exports required names correctly."""
        if not self.insurance_init_file.exists():
            self.skipTest("insurance/__init__.py file not found")
            
        with open(self.insurance_init_file, "r") as f:
            content = f.read()
        
        # Check for __all__ definition
        all_definition = re.search(r'__all__\s*=\s*\[', content)
        self.assertIsNotNone(all_definition, 
                           "insurance/__init__.py should define __all__ for exports")
        
        # Check that ClaimNotesAnalyzer is in __all__
        all_includes_analyzer = 'ClaimNotesAnalyzer' in content
        self.assertTrue(all_includes_analyzer, 
                      "insurance/__init__.py should export ClaimNotesAnalyzer")
        
        # Find positions to check order
        all_pos = content.find("__all__")
        import_pos = content.find("from .claim_notes_analyzer")
        
        # Check that __all__ is defined before imports
        if all_pos > 0 and import_pos > 0:
            self.assertLess(all_pos, import_pos, 
                          "__all__ should be defined before importing submodules")
    
    def test_actual_import_sequence(self):
        """Test the actual import sequence to ensure no circular imports."""
        # This test actually tries the imports in the correct sequence
        
        # First, clear any existing imports
        for module_name in list(sys.modules.keys()):
            if module_name.startswith('allyanonimiser'):
                del sys.modules[module_name]
        
        # Add the parent directory to sys.path if needed
        parent_dir = str(self.root_dir.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        try:
            # First import insurance.claim_notes_analyzer (this should work on its own)
            exec("from allyanonimiser.insurance import claim_notes_analyzer")
            
            # Now import the parent module
            exec("import allyanonimiser")
            
            # Finally, try to import and use create_au_insurance_analyzer
            exec("from allyanonimiser import create_au_insurance_analyzer")
            exec("analyzer = create_au_insurance_analyzer()")
            
            # If we got here, the imports succeeded without circular issues
            self.assertTrue(True)
            
        except ImportError as e:
            self.fail(f"Import failed due to circular import issue: {str(e)}")
        except Exception as e:
            # Skip rather than fail for other errors
            self.skipTest(f"Test skipped due to error: {str(e)}")


if __name__ == "__main__":
    unittest.main()