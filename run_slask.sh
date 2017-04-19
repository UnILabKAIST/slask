pushd /home/NoSyu/slack/slask
nohup /home/NoSyu/anaconda3/bin/python run_limbo.py >>slask_limbo.out 2>&1 &
echo $! >> slask_limbo.pid
popd
