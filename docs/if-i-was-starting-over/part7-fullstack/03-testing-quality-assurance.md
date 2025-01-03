# Chapter 3: Testing and Quality Assurance

## Introduction

Think about quality control in a car factory - you need to inspect parts, test assemblies, and verify the final product. Similarly, software development requires testing code, automating checks, and ensuring quality throughout the development process. In this chapter, we'll learn how to implement effective testing and quality assurance practices.

## 1. Testing Fundamentals

### The Car Inspection Metaphor

Think of testing like car inspection:
- Unit tests like part inspection
- Integration tests like system checks
- End-to-end tests like road tests
- Test coverage like inspection points
- Bug fixes like repairs

### Unit Testing

```python
# test_calculator.py
import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(1, 1), 0)
        self.assertEqual(self.calc.subtract(0, 5), -5)
    
    def test_multiply(self):
        self.assertEqual(self.calc.multiply(2, 3), 6)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 5), 0)
    
    def test_divide(self):
        self.assertEqual(self.calc.divide(6, 2), 3)
        self.assertEqual(self.calc.divide(5, 2), 2.5)
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```python
# test_user_service.py
import unittest
from services import UserService, EmailService, Database

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.email = EmailService()
        self.service = UserService(self.db, self.email)
    
    def test_user_registration(self):
        # Test complete registration flow
        user = self.service.register(
            'test@example.com',
            'password123'
        )
        
        # Verify user in database
        saved_user = self.db.get_user(user.id)
        self.assertEqual(saved_user.email, 'test@example.com')
        
        # Verify welcome email
        self.assertTrue(
            self.email.was_sent_to('test@example.com')
        )
    
    def test_login_flow(self):
        # Create test user
        user = self.service.register(
            'test@example.com',
            'password123'
        )
        
        # Test login
        session = self.service.login(
            'test@example.com',
            'password123'
        )
        
        # Verify session
        self.assertTrue(session.is_active)
        self.assertEqual(session.user_id, user.id)
    
    def tearDown(self):
        self.db.clear()
```

### Hands-On Exercise: Testing Framework

Create a testing framework:
```python
# testing_framework.py
import unittest
import json
from datetime import datetime

class TestCase:
    def __init__(self, name):
        self.name = name
        self.setup_called = False
        self.teardown_called = False
    
    def setUp(self):
        self.setup_called = True
    
    def tearDown(self):
        self.teardown_called = True
    
    def run(self):
        result = TestResult()
        result.test_started()
        
        try:
            self.setUp()
            method = getattr(self, self.name)
            method()
        except Exception as e:
            result.test_failed()
            result.error = str(e)
        else:
            result.test_passed()
        finally:
            self.tearDown()
        
        return result

class TestResult:
    def __init__(self):
        self.runs = 0
        self.failures = 0
        self.passes = 0
        self.error = None
        self.start_time = None
        self.end_time = None
    
    def test_started(self):
        self.runs += 1
        self.start_time = datetime.now()
    
    def test_failed(self):
        self.failures += 1
        self.end_time = datetime.now()
    
    def test_passed(self):
        self.passes += 1
        self.end_time = datetime.now()
    
    @property
    def duration(self):
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0
    
    def to_dict(self):
        return {
            'runs': self.runs,
            'failures': self.failures,
            'passes': self.passes,
            'error': self.error,
            'duration': self.duration
        }

class TestSuite:
    def __init__(self):
        self.tests = []
    
    def add(self, test):
        self.tests.append(test)
    
    def run(self):
        results = []
        for test in self.tests:
            results.append(test.run())
        return TestSuiteResult(results)

class TestSuiteResult:
    def __init__(self, results):
        self.results = results
    
    @property
    def total_runs(self):
        return sum(r.runs for r in self.results)
    
    @property
    def total_failures(self):
        return sum(r.failures for r in self.results)
    
    @property
    def total_passes(self):
        return sum(r.passes for r in self.results)
    
    @property
    def total_duration(self):
        return sum(r.duration for r in self.results)
    
    def to_dict(self):
        return {
            'total_runs': self.total_runs,
            'total_failures': self.total_failures,
            'total_passes': self.total_passes,
            'total_duration': self.total_duration,
            'results': [r.to_dict() for r in self.results]
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

# Example usage
class SimpleTest(TestCase):
    def test_addition(self):
        assert 2 + 2 == 4
    
    def test_subtraction(self):
        assert 4 - 2 == 2
    
    def test_failing(self):
        assert 2 + 2 == 5

# Run tests
suite = TestSuite()
suite.add(SimpleTest('test_addition'))
suite.add(SimpleTest('test_subtraction'))
suite.add(SimpleTest('test_failing'))

result = suite.run()
print(result.to_json())
```

## 2. Test Automation

### The Assembly Line Metaphor

Think of test automation like an assembly line:
- CI/CD like production line
- Test runners like quality stations
- Reports like inspection reports
- Coverage like inspection points
- Automation like robotic testing

### Setting Up CI/CD

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Upload coverage
      uses: actions/upload-artifact@v2
      with:
        name: coverage-report
        path: coverage/
```

### Test Runners

```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --verbose --cov=src --cov-report=html

# conftest.py
import pytest
from database import Database
from services import EmailService

@pytest.fixture
def db():
    """Provide test database."""
    db = Database('test.db')
    db.migrate()
    yield db
    db.clear()

@pytest.fixture
def email_service():
    """Provide mock email service."""
    return EmailService(test_mode=True)

# test_user_service.py
def test_registration(db, email_service):
    service = UserService(db, email_service)
    user = service.register('test@example.com', 'pass123')
    assert user.email == 'test@example.com'
    assert email_service.last_email.to == 'test@example.com'
```

### Hands-On Exercise: Test Suite

Create automated test suite:
```python
# test_suite.py
import pytest
import unittest
from datetime import datetime
import json
import coverage

class TestRunner:
    def __init__(self, test_dir='tests'):
        self.test_dir = test_dir
        self.results = []
        self.coverage = coverage.Coverage()
    
    def discover_tests(self):
        """Find all test files."""
        loader = unittest.TestLoader()
        return loader.discover(self.test_dir)
    
    def run_tests(self):
        """Run all tests with coverage."""
        # Start coverage
        self.coverage.start()
        
        # Run tests
        suite = self.discover_tests()
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Stop coverage
        self.coverage.stop()
        self.coverage.save()
        
        # Save results
        self.results = {
            'runs': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped),
            'success': result.wasSuccessful(),
            'coverage': self.get_coverage_data()
        }
        
        return self.results
    
    def get_coverage_data(self):
        """Get coverage statistics."""
        data = self.coverage.get_data()
        return {
            'total_statements': data.n_statements,
            'missing_statements': data.n_missing,
            'coverage_percent': data.percent_covered
        }
    
    def generate_report(self):
        """Generate test report."""
        if not self.results:
            raise ValueError("No test results available")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'results': self.results,
            'summary': {
                'total_tests': self.results['runs'],
                'passed': (
                    self.results['runs'] - 
                    self.results['failures'] - 
                    self.results['errors']
                ),
                'failed': self.results['failures'],
                'errors': self.results['errors'],
                'skipped': self.results['skipped'],
                'coverage': self.results['coverage']['coverage_percent']
            }
        }
        
        return json.dumps(report, indent=2)
    
    def save_report(self, filename='test_report.json'):
        """Save report to file."""
        report = self.generate_report()
        with open(filename, 'w') as f:
            f.write(report)

# Example tests
class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(2 + 2, 4)
    
    def test_subtraction(self):
        self.assertEqual(4 - 2, 2)
    
    @pytest.mark.skip("Example skip")
    def test_skipped(self):
        pass
    
    def test_error(self):
        raise ValueError("Example error")

# Run suite
if __name__ == '__main__':
    runner = TestRunner()
    results = runner.run_tests()
    runner.save_report()
    print(runner.generate_report())
```

## 3. Code Quality

### The Quality Control Metaphor

Think of code quality like product quality:
- Linting like visual inspection
- Style guides like manufacturing standards
- Documentation like product manuals
- Reviews like quality checks
- Metrics like quality measurements

### Code Style

```python
# .pylintrc
[MASTER]
ignore=CVS
persistent=yes
load-plugins=

[MESSAGES CONTROL]
disable=C0111,R0903,C0103

[REPORTS]
output-format=text
files-output=no
reports=no
evaluation=10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)

[BASIC]
good-names=i,j,k,ex,Run,_
bad-names=foo,bar,baz,toto,tutu,tata
name-group=
include-naming-hint=no
function-rgx=[a-z_][a-z0-9_]{2,30}$
variable-rgx=[a-z_][a-z0-9_]{2,30}$
const-rgx=(([A-Z_][A-Z0-9_]*)|(__.*__))$
attr-rgx=[a-z_][a-z0-9_]{2,30}$
argument-rgx=[a-z_][a-z0-9_]{2,30}$
class-attribute-rgx=([A-Za-z_][A-Za-z0-9_]{2,30}|(__.*__))$
inlinevar-rgx=[A-Za-z_][A-Za-z0-9_]*$
class-rgx=[A-Z_][a-zA-Z0-9]+$
module-rgx=(([a-z_][a-z0-9_]*)|([A-Z][a-zA-Z0-9]+))$
method-rgx=[a-z_][a-z0-9_]{2,30}$
no-docstring-rgx=__.*__
docstring-min-length=-1

[FORMAT]
max-line-length=100
ignore-long-lines=^\s*(# )?<?https?://\S+>?$
single-line-if-stmt=no
no-space-check=trailing-comma,dict-separator
max-module-lines=1000
indent-string='    '

[MISCELLANEOUS]
notes=FIXME,XXX,TODO

[SIMILARITIES]
min-similarity-lines=4
ignore-comments=yes
ignore-docstrings=yes
ignore-imports=no

[TYPECHECK]
ignore-mixin-members=yes
ignored-classes=SQLObject
unsafe-load-any-extension=yes

[VARIABLES]
init-import=no
dummy-variables-rgx=_$|dummy
additional-builtins=

[CLASSES]
ignore-iface-methods=isImplementedBy,deferred,extends,names,namesAndDescriptions,queryDescriptionFor,getBases,getDescriptionFor,getDoc,getName,getTaggedValue,getTaggedValueTags,isEqualOrExtendedBy,setTaggedValue,isImplementedByInstancesOf,adaptWith,is_implemented_by
defining-attr-methods=__init__,__new__,setUp
valid-classmethod-first-arg=cls
valid-metaclass-classmethod-first-arg=mcs

[DESIGN]
max-args=5
ignored-argument-names=_.*
max-locals=15
max-returns=6
max-branches=12
max-statements=50
max-parents=7
max-attributes=7
min-public-methods=2
max-public-methods=20

[IMPORTS]
deprecated-modules=regsub,TERMIOS,Bastion,rexec
import-graph=
ext-import-graph=
int-import-graph=

[EXCEPTIONS]
overgeneral-exceptions=Exception
```

### Documentation

```python
"""
User Service Module

This module provides user management functionality including:
- User registration
- Authentication
- Profile management
- Password reset

Example:
    service = UserService(database, email)
    user = service.register('user@example.com', 'password123')
    session = service.login('user@example.com', 'password123')
"""

from typing import Optional
from datetime import datetime
from .database import Database
from .email import EmailService

class UserService:
    """
    User management service.
    
    Handles all user-related operations including registration,
    authentication, and profile management.
    
    Attributes:
        db (Database): Database connection
        email (EmailService): Email service for notifications
    """
    
    def __init__(self, db: Database, email: EmailService):
        """
        Initialize service with required dependencies.
        
        Args:
            db: Database connection
            email: Email service for sending notifications
        """
        self.db = db
        self.email = email
    
    def register(self, email: str, password: str) -> User:
        """
        Register new user.
        
        Args:
            email: User's email address
            password: User's password (will be hashed)
        
        Returns:
            User: Created user object
        
        Raises:
            ValueError: If email already exists
            ValidationError: If password is too weak
        """
        if self.db.user_exists(email):
            raise ValueError("Email already registered")
        
        if not self._is_valid_password(password):
            raise ValidationError("Password too weak")
        
        user = User(
            email=email,
            password_hash=self._hash_password(password)
        )
        
        self.db.save_user(user)
        self.email.send_welcome(email)
        
        return user
```

### Hands-On Exercise: Quality Tools

Create quality checking tools:
```python
# quality_checker.py
import ast
import os
import re
from typing import List, Dict, Any
import json

class CodeAnalyzer:
    """Static code analysis tool."""
    
    def __init__(self, path: str):
        self.path = path
        self.issues = []
        self.stats = {
            'files': 0,
            'lines': 0,
            'functions': 0,
            'classes': 0,
            'comments': 0,
            'issues': 0
        }
    
    def analyze_file(self, filepath: str) -> None:
        """Analyze single file."""
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Update stats
        self.stats['files'] += 1
        self.stats['lines'] += len(content.splitlines())
        self.stats['comments'] += len(re.findall(r'#.*$', content, re.M))
        
        # Parse AST
        try:
            tree = ast.parse(content)
            self._analyze_node(tree, filepath)
        except SyntaxError as e:
            self.issues.append({
                'file': filepath,
                'line': e.lineno,
                'type': 'syntax_error',
                'message': str(e)
            })
    
    def _analyze_node(self, node: ast.AST, filepath: str) -> None:
        """Analyze AST node."""
        for child in ast.walk(node):
            # Count definitions
            if isinstance(child, ast.FunctionDef):
                self.stats['functions'] += 1
                self._check_function(child, filepath)
            elif isinstance(child, ast.ClassDef):
                self.stats['classes'] += 1
                self._check_class(child, filepath)
    
    def _check_function(self, node: ast.FunctionDef, filepath: str) -> None:
        """Check function definition."""
        # Check docstring
        if not ast.get_docstring(node):
            self.issues.append({
                'file': filepath,
                'line': node.lineno,
                'type': 'missing_docstring',
                'message': f'Function {node.name} missing docstring'
            })
        
        # Check arguments
        if len(node.args.args) > 5:
            self.issues.append({
                'file': filepath,
                'line': node.lineno,
                'type': 'too_many_arguments',
                'message': f'Function {node.name} has too many arguments'
            })
    
    def _check_class(self, node: ast.ClassDef, filepath: str) -> None:
        """Check class definition."""
        # Check docstring
        if not ast.get_docstring(node):
            self.issues.append({
                'file': filepath,
                'line': node.lineno,
                'type': 'missing_docstring',
                'message': f'Class {node.name} missing docstring'
            })
    
    def analyze(self) -> None:
        """Analyze all Python files in path."""
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    self.analyze_file(filepath)
        
        self.stats['issues'] = len(self.issues)
    
    def get_report(self) -> Dict[str, Any]:
        """Generate analysis report."""
        return {
            'stats': self.stats,
            'issues': self.issues
        }
    
    def save_report(self, filename: str = 'code_quality.json') -> None:
        """Save report to file."""
        report = self.get_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

class StyleChecker:
    """Code style checker."""
    
    def __init__(self):
        self.rules = {
            'max_line_length': 100,
            'indent_size': 4,
            'require_docstrings': True
        }
        self.violations = []
    
    def check_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Check file for style violations."""
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line.rstrip()) > self.rules['max_line_length']:
                self.violations.append({
                    'file': filepath,
                    'line': i,
                    'rule': 'max_line_length',
                    'message': 'Line too long'
                })
            
            # Check indentation
            indent = len(line) - len(line.lstrip())
            if indent % self.rules['indent_size'] != 0:
                self.violations.append({
                    'file': filepath,
                    'line': i,
                    'rule': 'indent_size',
                    'message': 'Invalid indentation'
                })
        
        return self.violations

class DocumentationChecker:
    """Documentation checker."""
    
    def check_docstrings(self, filepath: str) -> List[Dict[str, Any]]:
        """Check file for documentation issues."""
        issues = []
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return issues
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                docstring = ast.get_docstring(node)
                if not docstring:
                    issues.append({
                        'file': filepath,
                        'line': getattr(node, 'lineno', 1),
                        'type': 'missing_docstring',
                        'message': f'Missing docstring for {node.__class__.__name__}'
                    })
                elif docstring:
                    # Check docstring format
                    if not docstring.strip():
                        issues.append({
                            'file': filepath,
                            'line': getattr(node, 'lineno', 1),
                            'type': 'empty_docstring',
                            'message': f'Empty docstring for {node.__class__.__name__}'
                        })
                    elif not docstring.endswith('.'):
                        issues.append({
                            'file': filepath,
                            'line': getattr(node, 'lineno', 1),
                            'type': 'docstring_format',
                            'message': 'Docstring should end with period'
                        })
        
        return issues

# Example usage
if __name__ == '__main__':
    # Analyze code
    analyzer = CodeAnalyzer('src')
    analyzer.analyze()
    analyzer.save_report()
    
    # Check style
    style = StyleChecker()
    style_issues = style.check_file('src/main.py')
    
    # Check documentation
    docs = DocumentationChecker()
    doc_issues = docs.check_docstrings('src/main.py')
    
    # Print results
    print("Analysis complete!")
    print(f"Found {len(style_issues)} style issues")
    print(f"Found {len(doc_issues)} documentation issues")
```

## Practical Exercises

### 1. Test Suite
Build test system:
1. Unit tests
2. Integration tests
3. End-to-end tests
4. Test fixtures
5. Mock objects

### 2. CI Pipeline
Create pipeline with:
1. Automated tests
2. Code coverage
3. Style checks
4. Security scans
5. Performance tests

### 3. Quality Tools
Implement tools for:
1. Code analysis
2. Style checking
3. Documentation
4. Metrics
5. Reporting

## Review Questions

1. **Testing**
   - How write good tests?
   - When use different types?
   - Best practices for coverage?

2. **Automation**
   - How setup CI/CD?
   - When run tests?
   - Best practices for pipelines?

3. **Quality**
   - How measure quality?
   - When use tools?
   - Best practices for reviews?

## Additional Resources

### Online Tools
- Testing frameworks
- CI/CD platforms
- Code quality tools

### Further Reading
- Testing patterns
- Automation guides
- Quality metrics

### Video Resources
- Testing tutorials
- CI/CD guides
- Code quality

## Next Steps

After mastering these concepts, you'll be ready to:
1. Write effective tests
2. Automate processes
3. Maintain quality

Remember: Good testing ensures reliable software!

## Common Questions and Answers

Q: How much testing is enough?
A: Aim for high coverage of critical paths and edge cases.

Q: When should I automate tests?
A: Automate tests that are repetitive and important for reliability.

Q: How do I improve code quality?
A: Use tools, reviews, and consistent standards.

## Glossary

- **Test**: Code verification
- **Coverage**: Test scope
- **CI/CD**: Automation pipeline
- **Linting**: Style checking
- **Quality**: Code standards
- **Mock**: Test double
- **Fixture**: Test setup
- **Assert**: Test check
- **Report**: Test results
- **Metric**: Quality measure

Remember: Quality is a continuous process, not a one-time task!
