# pipy_publish.py
- prepare/install package
    pip install setuptools wheel
    pip install twine

- update info, version, descriptions,... in [prod] setup.py or [dev] setup-dev.py
- create/get token publish pipy https://pypi.org/manage/account/token/
- run sh script publish pipy
    [prod] ./pipy_publish.sh setup.py
    [dev]  ./pipy_publish.sh setup-dev.py
