This is not an officially supported Google product.

hanabi\_learning\_environment is a research platform for Hanabi experiments. The file rl\_env.py provides an RL environment using an API similar to OpenAI Gym. A lower level game interface is provided in pyhanabi.py for non-RL methods like Monte Carlo tree search.

### Getting started
```
sudo apt-get install g++         # if you don't already have a CXX compiler
sudo apt-get install python-pip  # if you don't already have pip
pip install .                    # or pip install git+repo_url to install directly from github

python rl_env_example.py         # Runs RL episodes
python game_example.py           # Plays a game using the lower level interface

### Rule based Agent
```
- in /hanabi_learning_environment/agents there is the rule_based_agent.py and the rules.py in which the rules for the agent are implemented

- in /hanabi_learning_environment there is the rl_env_example.py which is an expanded version of the file from /examples which is executable

- in /hanabi_learning_environment there is the rl_env_rule.py which is a slightly different version of the file above. This is also executable.
