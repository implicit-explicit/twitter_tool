# Implicit-Explicit Twitter Growth Hacking Tool

## Requirements
Python 3.5.1   
Python Twitter Tools (latest from git)   

Valid authorisation keys in 'auth_keys'. Format:
```
consumer_key
consumer_secret
```

## Usage
```
git clone https://github.com/implicit-explicit/twitter_tool.git
# optional: cd twitter_tool; py -m venv .venv
pip install -U -r requirements.txt
py twitter_tool.py {twitter handle w/o @} > results.txt
```
example: `py twitter_tool.py Im_Ex_plicit > implicit-explicit.txt`   

## Notes
`pip` will fetch latest PTT from the github repo. Latest changes don't seem to be on PyPi at the time of writing.   

The tool uses Application-Only Authorisation. It performs the necessary steps to create a bearer token file on first run, which will be used for the API requests. This will increase the rate limit slightly.   

## Tips
To only see the targets' followers count, you can use the following command:   
`py -c 'import twitter_tool; twitter_tool.target_info("Im_Ex_plicit")'`

The test file has a class to calculate the approximate time of operations: `RateLimitCalculationTestCase`.   
By default, running this test class uses a random followers count. Using the command above to only fetch followers count, you can edit the `self.followers` value and run `py -m unittest test.test_twitter_tool.RateLimitCalculationTestCase -v`

## References
Twitter API docs: [url](https://dev.twitter.com/overview/documentation)

## Licence
&copy; Implicit-Explicit