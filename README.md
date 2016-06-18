# Marathon Autoscaler

## Description

The aim of this project is to allow Marathon applications to scale to meet load requirements, without user intervention. To accomplish this, it monitors Marathon's application metrics and scales applications based on user-defined thresholds.


#### Table Of Contents

* [Build and deploy the Autoscaler](#build-and-deploy-the-autoscaler)
* [Run the Autoscaler](#run-the-autoscaler)
  * [Deploying the Autoscaler to Marathon](#deploying-the-autoscaler-to-marathon)
  * [Deploying a Marathon application to use the Autoscaler](#deploying-a-marathon-application-to-use-the-autoscaler)
    * [Participation](#participation)
    * [Minimum and Maximum Instances](#minimum-and-maximum-instances)
    * [Scaling Rules](#scaling-rules)
* [Testing the autoscaler with the Stress Tester app](#testing-the-autoscaler-with-the-stress-tester-app)


## Build and deploy the Autoscaler

The Makefile requires REGISTRY environment variable to be set to your Docker registry. 

```bash
REGISTRY=fooreg.mydockerregistry.com make
```

To manually build the app, the following commands build and deploy the Autoscaler Docker container: 

Build the python zipapp:

```bash
mkdir -p build/target
python -m zipapp lib/marathon-autoscaler -o build/target/marathon-autoscaler.pyz
```

Build the docker image:
```bash
docker build -t marathon_autoscaler .
```

Push the image to your registry:
```bash
docker push {{registry_url}}/marathon_autoscaler:latest
```

## Run the Autoscaler

### Deploying the Autoscaler to Marathon

In the `scripts` directory, deploy_autoscaler_to_marathon.py can be executed to deploy an 
instance of the Autoscaler to your Marathon system. The parameters needed are explained below:


| cli switch | environment variable | description |
|------------|----------------------|-------------|
| --interval | INTERVAL | The time duration in seconds between polling events |
| --mesos-uri | MESOS_URI | The Mesos HTTP endpoint |
| --mesos-agent-port | MESOS_AGENT_PORT | THe port your Mesos Agent is listening on (defaults to 5051) |
| --marathon-uri | MARATHON_URI | The Marathon HTTP endpoint |
| --marathon-user | MARATHON_USER | The Marathon username for authentication on the `marathon-uri` | 
| --marathon-pass | MARATHON_PASS | The Marathon password for authentication on the `marathon-uri` |
| --cpu-fan-out | CPU_FAN_OUT | Number of subprocesses to use for gathering and sending stats to Datadog |
| --dd-api-key | DATADOG_API_KEY | Datadog API key |
| --dd-app-key | DATADOG_APP_KEY | Datadog APP key |
| --dd-env | DATADOG_ENV | Datadog ENV variable to separate metrics by environment |
| --log-config | LOG_CONFIG | Path to logging configuration file. Defaults to logging_config.json |
| --enforce-version-match | ENFORCE_VERSION_MATCH | If set, version matching will be required of applications to participate |
| --rules-prefix | RULES_PREFIX | The prefix for rule names |

Run the script/deploy_autoscaler_to_marathon.py script:
```bash
cd script && python deploy_autoscaler_to_marathon.py {PARAMETERS}
```


### Deploying a Marathon application to use the Autoscaler 

#### Participation

The autoscaler is a standalone application that monitors Marathon for applications that use specific labels.  To make your application participate in the autoscaler the `use_marathon_autoscaler` label needs to be set to something truthful or a version number. To enable version matching, the autoscaler needs to be deployed with the `--enforce-version-match` commandline switch or `ENFORCE_VERSION_MATCH` environment variable.

The Autoscaler considers the following list of strings as true:

```python
["true", "t", "yes", "y", "1"]
```

#### Minimum and Maximum Instances

Number of minimum and maximum number of application instances.

```json
...
"labels": {
  "min_instances": 1,
  "max_instances": 10
}
...
```

#### Scaling Rules 

Scaling rules are set in a Marathon application's labels in its application definition. To get you introduced to scaling rules, let's jump right into an example:
```json
...
"labels": {
	"mas_rule_fastscaleup": "cpu | >90 | PT2M | 3 | PT1M30S"
},
...
```
Explanation: The above rule is called "fastscaleup" which states: if cpu is greater than\* 90 percent for 2 minutes, then scale up by 3 instances and backoff for 1 minute and 30 seconds\*\*. These values in the label value are the same as the original upper and lower thresholds, but you are no longer bound to stating both cpu and memory conditions.  The idea of having exclusive conditions is now implied by having multiple rules with the same name. Here's an example of the above rule added to other conditions:

```json
...
"labels": {
	"mas_rule_fastscaleup_1": "cpu | >90 | PT2M | 3 | PT1M30S",
	"mas_rule_fastscaleup_2": "memory | >85 | PT2M | 3 | PT1M30S"
},
...
```
Notice that the tolerance, scale factor and backoff values are repeated, this is for clarity, but when the autoscaler sees 2 or more rules with the same name, it will combine them into one rule and use the tolerance, scale factor, and backoff of the first rule it sees. In the example above, the suffix "_1" and "_2" are for Marathon's sake because Marathon does not support having repeat label names. If this suffix is numeric, the autoscaler will order them numerically and take the tolerance, scale factor and backoff from the mas_rule_fastscale_1 rule.

To complete the example above, so it contains scale down rules, here is example extended:
```json
...
"labels": {
	"mas_rule_fastscaleup_1": "cpu | >90 | PT2M | 3 | PT1M30S",
	"mas_rule_fastscaleup_2": "memory | >85 | PT2M | 3 | PT1M30S",
	"mas_rule_slowscaledown_1": "cpu | <=90 | PT1M | 1 | PT30S",
	"mas_rule_slowscaledown_2": "memory | <=85 | PT1M | 1 | PT30S"
},
...
```

Let's explore some other ideas...
Maybe your application is only interested in scaling based on CPU:

```json
...
"labels": {
	"mas_rule_fastscaleup": "cpu | >90 | PT2M | 3 | PT1M30S",
	"mas_rule_slowscaledown": "cpu | <=90 | PT1M | 1 | PT30S",
},
...
```

Perhaps you want your application to scale up and down differently for different conditions:
```json
...
"labels": {
	"mas_rule_slowscaleup": "cpu | >40 | PT2M | 1 | PT1M30S",
	"mas_rule_fastscaleup": "cpu | >60 | PT1M | 3 | PT30S",
	"mas_rule_hyperscaleup": "cpu | >90 | PT1M | 5 | PT15S",
	"mas_rule_slowscaledown": "cpu | <90 | PT1M30S | 1 | PT30S",
	"mas_rule_fastscaledown": "cpu | <10 | PT3M | 5 | PT30S",
},
...
```
When multiple rules focus on the same metric, the autoscaler should take the action of the rule that matches closest to the given tolerance and threshold. It is possible that your application may never trigger some rules depending on the application's behavior.
 

\* Comparisons can use >, <, <=, >=, = or ==
 
\*\* [A Wikipedia Reference on ISO8601 time duration](https://en.wikipedia.org/wiki/ISO_8601#Durations)



## Testing the autoscaler with the Stress Tester app

To see how the Autoscaler behaves with an application's scaling settings in a controlled environment, build and deploy the stress test application to an environment running the Autoscaler.

```bash
cd tests/stress_tester_app && docker build -t autoscale_test_app .
```

Push the image to the registry:
```bash
docker push autoscale_test_app:latest
```

Run the script/test_autoscaler.py script:
```bash
cd script && python test_autoscaler.py --marathon-uri MARATHON_HTTP --marathon-user MARATHON_USER --marathon-pass MARATHON_PASS
```
