import numpy as np

# AND 연산
class AndPerceptron:
    def __init__(self):
        self.weights = np.random.rand(2)
        self.bias = np.random.rand(1)

    def train(self, inputs, outputs, learning_rate=0.1, epochs=20):
        for epoch in range(epochs):
            for i in range(len(inputs)):
                total_input = np.dot(inputs[i], self.weights) + self.bias
                prediction = self._step_function(total_input)
                error = outputs[i] - prediction
                self.weights += learning_rate * error * inputs[i]
                self.bias += learning_rate * error

    def predict(self, input_data):
        total_input = np.dot(input_data, self.weights) + self.bias
        return self._step_function(total_input)

    def _step_function(self, x):
        return 1 if x >= 0 else 0

# NOT 연산
class NotPerceptron:
    def __init__(self):
        self.weight = np.random.rand(1)
        self.bias = np.random.rand(1)

    def train(self, inputs, outputs, learning_rate=0.1, epochs=20):
        for epoch in range(epochs):
            for i in range(len(inputs)):
                total_input = np.dot(inputs[i], self.weight) + self.bias
                prediction = self._step_function(total_input)
                error = outputs[i] - prediction
                self.weight += learning_rate * error * inputs[i]
                self.bias += learning_rate * error

    def predict(self, input_data):
        total_input = np.dot(input_data, self.weight) + self.bias
        return self._step_function(total_input)

    def _step_function(self, x):
        return 1 if x >= 0 else 0

# XOR 연산 (단층 퍼셉트론으로는 불가능)
# 다층 퍼셉트론(MLP)을 사용해야 함
class XorPerceptron:
    def __init__(self):
        # 2개의 입력층, 2개의 은닉층, 1개의 출력층
        self.weights1 = np.random.rand(2, 2)
        self.bias1 = np.random.rand(2)
        self.weights2 = np.random.rand(2, 1)
        self.bias2 = np.random.rand(1)

    def train(self, inputs, outputs, learning_rate=0.1, epochs=10000): # epochs 값 조정
        for epoch in range(epochs):
            for i in range(len(inputs)):
                # 순전파
                hidden_output = self._step_function(np.dot(inputs[i], self.weights1) + self.bias1)
                final_output = self._step_function(np.dot(hidden_output, self.weights2) + self.bias2)
                # 오차 계산
                error = outputs[i] - final_output
                # 역전파 (간소화)
                self.weights2 += learning_rate * error * hidden_output.reshape(2, 1)
                self.bias2 += learning_rate * error
                error_hidden = error * self.weights2.reshape(2,)
                self.weights1 += learning_rate * error_hidden * inputs[i].reshape(2, 1)
                self.bias1 += learning_rate * error_hidden

    def predict(self, input_data):
        hidden_output = self._step_function(np.dot(input_data, self.weights1) + self.bias1)
        final_output = self._step_function(np.dot(hidden_output, self.weights2) + self.bias2)
        return final_output

    def _step_function(self, x):
        return (x >= 0).astype(int)