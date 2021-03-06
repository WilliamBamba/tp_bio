import argparse
import sys
from random import sample 
import gym
from gym import wrappers, logger
from collections import deque



class RandomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('env_id', nargs='?', default='CartPole-v1', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = '/tmp/random-agent-results'
    env = wrappers.Monitor(env, directory=outdir, force=True)
    env.seed(0)
    agent = RandomAgent(env.action_space)

    episode_count = 100
    reward = 0
    done = False
    ep_reward_sum = 0
    size = 100
    d = deque([], size)



    for i in range(episode_count):
        print("Final reward : " + str(ep_reward_sum) + " Episode : "+ str(i))
        ep_reward_sum = 0
        state = env.env.state
        ob = env.reset()
        while True:
            action = agent.act(ob, reward, done)
            ob, reward, done, _ = env.step(action)
            ep_reward_sum += reward
            new_state = env.env.state
            if(len(d) == size):
                d.popleft() 
            d.append((state,action,new_state,reward,done))
            if done:
                break
            # Note there's no env.render() here. But the environment still can open window and
            # render if asked by env.monitor: it calls env.render('rgb_array') to record video.
            # Video is not recorded every episode, see capped_cubic_video_schedule for details.
    minibatch = sample(d,20)
    print(" Interractions : "+str(minibatch))
    
    # Close the env and write monitor result info to disk
    env.close()