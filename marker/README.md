# 설치

```
# pytorch docker 환경에서
$ pip install marker-pdf
```

# 실행

```
# single file
$ marker_single /path/to/file.pdf /path/to/output/folder --batch_multiplier 2 --max_pages 10 --langs English

# multiple-files
$ marker /path/to/input/folder /path/to/output/folder --workers 10 --max 10 --metadata_file /path/to/metadata.json --min_length 10000
```

# 참고

[github](https://github.com/VikParuchuri/marker)
