# JIRA API with PHP Examples

## Table of Contents
- [JIRA API with PHP Examples](#jira-api-with-php-examples)
  - [Examples Overview](#examples-overview)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Basic Operations](#basic-operations)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Examples Overview

1. Basic Operations
   - Authentication and connection
   - Issue CRUD operations
   - Project management
   - User management

2. Advanced Features
   - Custom field handling
   - Workflow automation
   - Bulk operations
   - Attachments handling

3. Integration Features
   - Webhook handling
   - Custom field sync
   - External tool integration
   - Reporting automation

4. Full Applications
   - Issue tracker dashboard
   - Project management tool
   - Reporting system
   - Workflow automator

## Project Structure

```
php/
├── basic/
│   ├── authentication/
│   │   ├── index.php
│   │   ├── composer.json
│   │   └── config.php
│   ├── issues/
│   ├── projects/
│   └── users/
├── advanced/
│   ├── workflows/
│   ├── custom_fields/
│   ├── bulk_operations/
│   └── attachments/
├── integration/
│   ├── webhooks/
│   ├── field_sync/
│   ├── external_tools/
│   └── reporting/
└── applications/
    ├── issue_dashboard/
    ├── project_manager/
    ├── report_generator/
    └── workflow_automator/
```

## Getting Started

1. Install Dependencies:
```bash
composer require lesstif/php-jira-rest-client
```

2. Configure JIRA Connection:
```php
<?php
// config.php
return [
    'jira' => [
        'host' => 'https://your-domain.atlassian.net',
        'username' => 'your-email@example.com',
        'password' => 'your-api-token',
        'api_version' => '3',
        'verify' => true
    ]
];
```

3. Basic Setup:
```php
<?php
require 'vendor/autoload.php';

use JiraRestApi\Configuration\ArrayConfiguration;
use JiraRestApi\Issue\IssueService;

$config = new ArrayConfiguration(require 'config.php');
```

## Basic Operations

### Authentication and Connection
```php
<?php
class JiraClient {
    private $config;
    
    public function __construct() {
        $this->config = new ArrayConfiguration([
            'jira' => [
                'host' => getenv('JIRA_HOST'),
                'username' => getenv('JIRA_USERNAME'),
                'password' => getenv('JIRA_API_TOKEN')
            ]
        ]);
    }
    
    public function testConnection() {
        try {
            $issueService = new IssueService($this->config);
            $issue = $issueService->get('TEST-1');
            return true;
        } catch (Exception $e) {
            error_log("Connection failed: " . $e->getMessage());
            return false;
        }
    }
}
```

### Issue Management
```php
<?php
class IssueManager {
    private $issueService;
    
    public function __construct($config) {
        $this->issueService = new IssueService($config);
    }
    
    public function createIssue($projectKey, $summary, $description, $issueType = 'Task') {
        $issueField = new IssueField();
        
        $issueField->setProjectKey($projectKey)
                   ->setSummary($summary)
                   ->setDescription($description)
                   ->setIssueType($issueType);
        
        return $this->issueService->create($issueField);
    }
    
    public function updateIssue($issueKey, $fields) {
        $issueField = new IssueField(true);
        
        foreach ($fields as $key => $value) {
            $issueField->$key = $value;
        }
        
        return $this->issueService->update($issueKey, $issueField);
    }
    
    public function transitionIssue($issueKey, $transitionName) {
        $transition = $this->findTransition($issueKey, $transitionName);
        if ($transition) {
            return $this->issueService->transition($issueKey, $transition);
        }
        throw new Exception("Transition '$transitionName' not found");
    }
    
    private function findTransition($issueKey, $transitionName) {
        $transitions = $this->issueService->getTransitions($issueKey);
        foreach ($transitions as $transition) {
            if (strtolower($transition['name']) === strtolower($transitionName)) {
                return $transition;
            }
        }
        return null;
    }
}
```

## Advanced Features

### Custom Field Management
```php
<?php
class CustomFieldManager {
    private $fieldService;
    private $issueService;
    
    public function __construct($config) {
        $this->fieldService = new FieldService($config);
        $this->issueService = new IssueService($config);
    }
    
    public function getCustomFieldId($fieldName) {
        $fields = $this->fieldService->getAllFields();
        foreach ($fields as $field) {
            if ($field['name'] === $fieldName) {
                return $field['id'];
            }
        }
        return null;
    }
    
    public function updateCustomField($issueKey, $fieldName, $value) {
        $fieldId = $this->getCustomFieldId($fieldName);
        if (!$fieldId) {
            throw new Exception("Custom field '$fieldName' not found");
        }
        
        $issueField = new IssueField(true);
        $issueField->$fieldId = $value;
        
        return $this->issueService->update($issueKey, $issueField);
    }
}
```

### Workflow Automation
```php
<?php
class WorkflowAutomator {
    private $issueService;
    
    public function __construct($config) {
        $this->issueService = new IssueService($config);
    }
    
    public function autoAssignIssues($projectKey, $assigneeMap) {
        $jql = "project = $projectKey AND assignee IS EMPTY";
        $issues = $this->issueService->search($jql);
        
        foreach ($issues->getIssues() as $issue) {
            $component = $issue->fields->components[0]->name ?? null;
            if ($component && isset($assigneeMap[$component])) {
                $issueField = new IssueField(true);
                $issueField->setAssignee($assigneeMap[$component]);
                $this->issueService->update($issue->key, $issueField);
            }
        }
    }
    
    public function autoTransitionIssues($projectKey, $conditions) {
        foreach ($conditions as $condition) {
            $jql = "project = $projectKey AND {$condition['jql']}";
            $issues = $this->issueService->search($jql);
            
            foreach ($issues->getIssues() as $issue) {
                try {
                    $this->transitionIssue(
                        $issue->key,
                        $condition['transition']
                    );
                } catch (Exception $e) {
                    error_log("Failed to transition {$issue->key}: {$e->getMessage()}");
                }
            }
        }
    }
}
```

## Security Considerations

1. Token Management:
```php
<?php
class TokenManager {
    private $key;
    
    public function __construct() {
        $this->key = getenv('ENCRYPTION_KEY');
    }
    
    public function encryptToken($token) {
        $cipher = "aes-256-gcm";
        $ivlen = openssl_cipher_iv_length($cipher);
        $iv = openssl_random_pseudo_bytes($ivlen);
        
        $tag = "";
        $encrypted = openssl_encrypt(
            $token,
            $cipher,
            $this->key,
            OPENSSL_RAW_DATA,
            $iv,
            $tag
        );
        
        return base64_encode($iv . $tag . $encrypted);
    }
    
    public function decryptToken($encryptedToken) {
        $cipher = "aes-256-gcm";
        $data = base64_decode($encryptedToken);
        
        $ivlen = openssl_cipher_iv_length($cipher);
        $iv = substr($data, 0, $ivlen);
        $tag = substr($data, $ivlen, 16);
        $encrypted = substr($data, $ivlen + 16);
        
        return openssl_decrypt(
            $encrypted,
            $cipher,
            $this->key,
            OPENSSL_RAW_DATA,
            $iv,
            $tag
        );
    }
}
```

2. Request Validation:
```php
<?php
class WebhookValidator {
    public static function validateRequest($request) {
        $token = $request->header('X-Atlassian-Token');
        if (!$token || $token !== 'no-check') {
            throw new Exception('Invalid webhook token');
        }
        
        return true;
    }
}

// Usage in route
Route::post('/webhook/jira', function (Request $request) {
    try {
        WebhookValidator::validateRequest($request);
        // Process webhook
        return response('', 200);
    } catch (Exception $e) {
        return response($e->getMessage(), 403);
    }
});
```

## Performance Optimization

1. Batch Processing:
```php
<?php
class BatchProcessor {
    private $issueService;
    
    public function __construct($config) {
        $this->issueService = new IssueService($config);
    }
    
    public function bulkCreateIssues($issues, $batchSize = 50) {
        $results = [];
        foreach (array_chunk($issues, $batchSize) as $batch) {
            $bulkIssueFields = [];
            foreach ($batch as $issue) {
                $issueField = new IssueField();
                $issueField->setProjectKey($issue['project'])
                          ->setSummary($issue['summary'])
                          ->setDescription($issue['description'])
                          ->setIssueType($issue['type']);
                $bulkIssueFields[] = $issueField;
            }
            $results = array_merge(
                $results,
                $this->issueService->createMultiple($bulkIssueFields)
            );
        }
        return $results;
    }
}
```

2. Caching:
```php
<?php
class CachedJiraClient {
    private $cache;
    private $issueService;
    
    public function __construct($config) {
        $this->cache = new Redis();
        $this->cache->connect('127.0.0.1', 6379);
        $this->issueService = new IssueService($config);
    }
    
    public function getIssue($issueKey) {
        $cacheKey = "issue:$issueKey";
        $cached = $this->cache->get($cacheKey);
        
        if ($cached) {
            return json_decode($cached);
        }
        
        $issue = $this->issueService->get($issueKey);
        $this->cache->setex($cacheKey, 300, json_encode($issue));
        
        return $issue;
    }
}
```

## Testing

1. Unit Tests:
```php
<?php
use PHPUnit\Framework\TestCase;

class JiraTest extends TestCase {
    private $issueManager;
    
    protected function setUp(): void {
        $config = new ArrayConfiguration(require 'config.php');
        $this->issueManager = new IssueManager($config);
    }
    
    public function testCreateIssue() {
        $issue = $this->issueManager->createIssue(
            'TEST',
            'Test Issue',
            'Description'
        );
        
        $this->assertNotNull($issue->key);
        $this->assertEquals('Test Issue', $issue->fields->summary);
    }
}
```

2. Integration Tests:
```php
<?php
class JiraIntegrationTest extends TestCase {
    private $issueService;
    
    protected function setUp(): void {
        $config = new ArrayConfiguration(require 'config.php');
        $this->issueService = new IssueService($config);
    }
    
    public function testIssueWorkflow() {
        // Create issue
        $issueField = new IssueField();
        $issueField->setProjectKey('TEST')
                   ->setSummary('Integration Test')
                   ->setIssueType('Task');
        
        $issue = $this->issueService->create($issueField);
        
        // Update issue
        $updateField = new IssueField(true);
        $updateField->setDescription('Updated description');
        $this->issueService->update($issue->key, $updateField);
        
        // Verify changes
        $updated = $this->issueService->get($issue->key);
        $this->assertEquals(
            'Updated description',
            $updated->fields->description
        );
        
        // Clean up
        $this->issueService->delete($issue->key);
    }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
