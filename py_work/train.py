import numpy as np
import random
import sys
from game import SnakeGame
from model import build_model
from replay_buffer import ReplayBuffer

def train_dqn(episodes, target_score=200, patience=50):
    gamma = 0.95
    epsilon = 1.0
    epsilon_min = 0.01
    epsilon_decay = 0.995
    batch_size = 32

    env = SnakeGame()
    state_size = env.get_state().shape[0]
    action_size = 3  # [Straight, Right turn, Left turn]

    model = build_model(state_size, action_size)
    target_model = build_model(state_size, action_size)
    target_model.set_weights(model.get_weights())

    replay_buffer = ReplayBuffer(max_size=2000)

    best_score = -float('inf')
    patience_counter = 0

    for episode in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        total_reward = 0

        for time in range(500):
            env.handle_events()  # Handle window close event

            action = np.argmax(model.predict(state)[0]) if np.random.rand() > epsilon else random.randrange(action_size)
            next_state, reward, done = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])

            replay_buffer.add((state, action, reward, next_state, done))
            state = next_state
            total_reward += reward

            if done:
                target_model.set_weights(model.get_weights())
                print(f"Episode: {episode+1}/{episodes}, Score: {env.score}, Epsilon: {epsilon:.2}")
                break

            if replay_buffer.size() > batch_size:
                minibatch = replay_buffer.sample(batch_size)
                for state, action, reward, next_state, done in minibatch:
                    target = reward
                    if not done:
                        target += gamma * np.amax(target_model.predict(next_state)[0])
                    target_f = model.predict(state)
                    target_f[0][action] = target
                    model.fit(state, target_f, epochs=1, verbose=0)

            if epsilon > epsilon_min:
                epsilon *= epsilon_decay

        if total_reward > best_score:
            best_score = total_reward
            patience_counter = 0
        else:
            patience_counter += 1

        if patience_counter >= patience:
            print(f"Training stopped early after {episode+1} episodes due to lack of improvement.")
            break

if __name__ == "__main__":
    train_dqn(1000)
