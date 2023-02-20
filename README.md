# RASA from the scratch 
```
$ rasa init
$ rasa train nlu
$ rasa shell nlu
```

# Run the api server
- run rasa after running the action server
- specify device index if it exists
```
rasa run actions
cuda_visible_devices=1 rasa run --enable-api
```

# Branch Policy
- develop_meong: branch for meong service

