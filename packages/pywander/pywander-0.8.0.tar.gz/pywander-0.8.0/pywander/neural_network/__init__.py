"""
神经网络

"""
import numpy as np
from scipy.special import expit
from pywander.math.linear_algebra import to_row_vector, row_vector_to_column_vector, to_column_vector


class NeuralNetwork:
    def __init__(self, input_nodes=1, output_nodes=1, learning_rate=0.3, val_range=(0.01, 0.99)):
        # 权重、信号的值的约束范围
        self.val_range = val_range
        # 输入层节点数
        self.i_nodes = input_nodes
        # 输出层节点数
        self.o_nodes = output_nodes
        # label 任何神经网络都有其判断标识 只是有些和外界发生了对齐行为
        # 只有发生对齐行为的神经网络才会有训练行为
        self.label_list = ['' for _ in range(self.o_nodes)]
        self.label_out = []
        self.init_label_out()

        # 学习率
        self.lr = learning_rate

    def init_label_out(self):
        self.label_out = np.eye(self.o_nodes)

    def set_label_list(self, label_list):
        assert len(label_list) == self.o_nodes
        self.label_list = label_list

    def get_label_out(self, label):
        index = self.label_list.index(label)
        return self.label_out[index]

    def train(self, *args, **kwargs):
        pass

    def query(self, input_array):
        pass

    def pre_process_input2(self, input_array):
        # 输入信号归一化
        norm = np.linalg.norm(input_array)
        input_array = input_array / norm
        return input_array

    def pre_process_input(self, input_array):
        input_array = scale_to_range(input_array, min_val=self.val_range[0], max_val=self.val_range[1])
        return input_array


class SimpleFNN2(NeuralNetwork):
    """
    单隐藏层前馈神经网络
    无激活函数 归一化之后仍然效果比不上有激活函数的
    """

    def __init__(self, input_nodes=1, output_nodes=1, hidden_nodes=1, learning_rate=0.3):
        super().__init__(input_nodes=input_nodes, output_nodes=output_nodes, learning_rate=learning_rate)
        # 隐藏层节点数
        self.h_nodes = hidden_nodes

        # 权重矩阵随机生成
        self.weight_matrix_hidden_output = None
        self.weight_matrix_input_hidden = None
        self.init_weight_matrix2()

    def init_weight_matrix(self):
        """
        经过一些实践就会发现初始权重矩阵有一些小技巧和注意事项，然后总的来说不太重要，因此不需要精确
        """
        self.weight_matrix_input_hidden = np.random.rand(self.h_nodes, self.i_nodes) - 0.5
        self.weight_matrix_hidden_output = np.random.rand(self.o_nodes, self.h_nodes) - 0.5

    def init_weight_matrix2(self):
        """
        以0为中心的正态分布采样
        """
        self.weight_matrix_input_hidden = np.random.normal(
            0.0, pow(self.h_nodes, -0.5), (self.h_nodes, self.i_nodes))
        self.weight_matrix_hidden_output = np.random.normal(
            0.0, pow(self.o_nodes, -0.5), (self.o_nodes, self.h_nodes))

    def query(self, input_array):
        input_array = self.pre_process_input2(input_array)

        hidden_input = np.dot(self.weight_matrix_input_hidden, input_array)
        # hidden_output = self.activation_function(hidden_input)
        hidden_output = hidden_input
        final_inputs = np.dot(self.weight_matrix_hidden_output, hidden_output)
        # final_outputs = self.activation_function(final_inputs)
        final_outputs = final_inputs
        return final_outputs

    def query_label(self, intput_array):
        final_outputs = self.query(intput_array)
        index = np.argmax(final_outputs)
        return self.label_list[index]

    def train(self, input_array, label):
        input_array = self.pre_process_input2(input_array)

        hidden_input = np.dot(self.weight_matrix_input_hidden, input_array)
        # hidden_output = self.activation_function(hidden_input)
        hidden_output = hidden_input
        final_inputs = np.dot(self.weight_matrix_hidden_output, hidden_output)
        # final_outputs = self.activation_function(final_inputs)
        final_outputs = final_inputs

        target_label_out = self.get_label_out(label)
        error_output = target_label_out - final_outputs

        error_hidden = np.dot(self.weight_matrix_hidden_output.transpose(), error_output)

        self.weight_matrix_hidden_output += self.lr * np.dot(to_column_vector(error_output),
                                                             to_row_vector(hidden_output))

        self.weight_matrix_input_hidden += self.lr * np.dot(to_column_vector(error_hidden), to_row_vector(input_array))

    def init_weight_matrix_old(self, init_array):
        """
        初始权重
        """
        column_vector_output = np.array([[1]])
        row_vector_hidden = np.random.rand(self.h_nodes)
        row_vector_hidden = to_row_vector(row_vector_hidden)
        # 隐藏层输出信号归一化 使得modifiers=1
        norm = np.linalg.norm(row_vector_hidden)
        row_vector_hidden = row_vector_hidden / norm
        column_vector_hidden = row_vector_to_column_vector(row_vector_hidden)

        # res = np.dot(row_vector_hidden, row_vector_hidden.transpose())
        # modifiers = res[0][0]

        self.weight_matrix_hidden_output = np.dot(column_vector_output, row_vector_hidden)
        # self.weight_matrix_hidden_output = self.weight_matrix_hidden_output / modifiers

        # 输入信号归一化 使得modifiers=1
        row_vector_input = to_row_vector(np.asarray(init_array, dtype=float))
        norm = np.linalg.norm(row_vector_input)
        row_vector_input = row_vector_input / norm
        # res = np.dot(row_vector_input, row_vector_input.transpose())
        # modifiers = res[0][0]

        self.weight_matrix_input_hidden = np.dot(column_vector_hidden, row_vector_input)
        # self.weight_matrix_input_hidden = self.weight_matrix_input_hidden / modifiers


class SimpleFNN(NeuralNetwork):
    """
    单隐藏层前馈神经网络
    有激活函数
    """

    def __init__(self, input_nodes=1, output_nodes=1, hidden_nodes=1, learning_rate=0.3):
        super().__init__(input_nodes=input_nodes, output_nodes=output_nodes, learning_rate=learning_rate)
        # 隐藏层节点数
        self.h_nodes = hidden_nodes

        # 权重矩阵随机生成
        self.weight_matrix_hidden_output = None
        self.weight_matrix_input_hidden = None
        self.init_weight_matrix2()

        # 激活函数
        self.activation_function = lambda x: expit(x)

    def init_label_out(self):
        label_out = np.eye(self.o_nodes)
        label_out = scale_to_range(label_out, min_val=self.val_range[0], max_val=self.val_range[1])
        self.label_out = label_out

    def init_weight_matrix(self):
        """
        经过一些实践就会发现初始权重矩阵有一些小技巧和注意事项，然后总的来说不太重要，因此不需要精确
        """
        self.weight_matrix_input_hidden = np.random.rand(self.h_nodes, self.i_nodes) - 0.5
        self.weight_matrix_hidden_output = np.random.rand(self.o_nodes, self.h_nodes) - 0.5

    def init_weight_matrix2(self):
        """
        以0为中心的正态分布采样
        """
        self.weight_matrix_input_hidden = np.random.normal(
            0.0, pow(self.h_nodes, -0.5), (self.h_nodes, self.i_nodes))
        self.weight_matrix_hidden_output = np.random.normal(
            0.0, pow(self.o_nodes, -0.5), (self.o_nodes, self.h_nodes))

    def query(self, input_array):
        input_array = self.pre_process_input(input_array)

        hidden_input = np.dot(self.weight_matrix_input_hidden, input_array)
        hidden_output = self.activation_function(hidden_input)

        final_inputs = np.dot(self.weight_matrix_hidden_output, hidden_output)
        final_outputs = self.activation_function(final_inputs)

        return final_outputs

    def query_label(self, input_array):
        final_outputs = self.query(input_array)
        index = np.argmax(final_outputs)
        return self.label_list[index]

    def train(self, input_array, label):
        input_array = self.pre_process_input(input_array)

        hidden_input = np.dot(self.weight_matrix_input_hidden, input_array)
        hidden_output = self.activation_function(hidden_input)

        final_inputs = np.dot(self.weight_matrix_hidden_output, hidden_output)
        final_outputs = self.activation_function(final_inputs)

        target_label_out = self.get_label_out(label)
        error_output = target_label_out - final_outputs

        error_hidden = np.dot(self.weight_matrix_hidden_output.transpose(), error_output)

        self.weight_matrix_hidden_output += self.lr * np.dot(
            to_column_vector(error_output * final_outputs * (1 - final_outputs)),
            to_row_vector(hidden_output))

        self.weight_matrix_input_hidden += self.lr * np.dot(
            to_column_vector(error_hidden * hidden_output * (1 - hidden_output)), to_row_vector(input_array))


def scale_to_range(arr, min_val=0.001, max_val=0.999):
    """
    将数组中的所有数字缩放到指定的范围 [min_val, max_val]
    :param arr: 输入的 numpy 数组
    :param min_val: 缩放后的最小值
    :param max_val: 缩放后的最大值
    :return: 缩放后的 numpy 数组
    """
    # 找到数组中的最小值和最大值
    arr_min = np.min(arr)
    arr_max = np.max(arr)
    # 进行线性缩放
    scaled_arr = min_val + (arr - arr_min) / (arr_max - arr_min) * (max_val - min_val)
    return scaled_arr


def load_mnist_csv_data(filename):
    data = []

    with open(filename) as f:
        for line in f:
            label = line[0]
            image_data = line[2:]
            image_data = image_data.strip()
            image_data_list = image_data.split(',')
            image_data2 = np.asarray(image_data_list, dtype=float)

            data.append((label, image_data2))

    return data


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)


    def test_simple_fnn2():

        nn = SimpleFNN2(input_nodes=28 * 28, output_nodes=10, hidden_nodes=100, learning_rate=0.2)
        label_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        nn.set_label_list(label_list)

        train_data = load_mnist_csv_data('mnist_dataset/mnist_train.csv')
        test_data = load_mnist_csv_data('mnist_dataset/mnist_test.csv')

        score_card = []

        for label, value in train_data:
            nn.train(value, label)

        for label, value in test_data:
            result_label = nn.query_label(value)

            if label == result_label:
                score_card.append(1)
            else:
                score_card.append(0)

        score_card = np.asarray(score_card)
        print(score_card.sum() / score_card.size)

        print('################################################')


    def test_simple_fnn():
        epochs = 5
        learning_rate = 0.2 / epochs

        nn = SimpleFNN(input_nodes=28 * 28, output_nodes=10, hidden_nodes=100, learning_rate=learning_rate)
        label_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        nn.set_label_list(label_list)

        train_data = load_mnist_csv_data('mnist_dataset/mnist_train.csv')
        test_data = load_mnist_csv_data('mnist_dataset/mnist_test.csv')

        score_card = []

        for e in range(epochs):
            for label, value in train_data:
                nn.train(value, label)

            print(f'epoch {e} finished....')

        for label, value in test_data:
            result_label = nn.query_label(value)

            if label == result_label:
                score_card.append(1)
            else:
                score_card.append(0)

        score_card = np.asarray(score_card)
        print(score_card.sum() / score_card.size)
        print('################################################')


    test_simple_fnn()
