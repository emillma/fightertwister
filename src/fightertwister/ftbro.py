import numpy as np
from .fightertwister import FighterTwister
from .encoder import Encoder
from .button import Button
from .utils import ft_colors


class FtBro(FighterTwister):
    def __init__(self):
        super().__init__()
        self.indicator_brightness_on = 1
        self.indicator_brightness_off = 0.4

        self.color_selected = ft_colors.green
        self.color_copy = ft_colors.yellow
        self.color_node_default = ft_colors.blue
        self.color_param_default = ft_colors.magenta
        self.copy_param = (2, 0)
        self.enc_nodes = self.encoders[0, :2, :]
        self.enc_params = self.encoders[0, 2:, :]
        self.data = np.zeros((*self.enc_nodes.shape, *self.enc_params.shape))
        self.current_node = (0, 0)

        self.noeds_on = np.zeros(self.enc_nodes.shape, int)
        self.selected_for_copy = np.zeros(self.enc_nodes.shape, int)

        self.enc_nodes.set_delay_hold(200)

        self.enc_nodes.register_cb_hold(self.node_hold)
        self.enc_nodes.register_cb_click(self.toggle_onoff)
        self.enc_nodes.register_cb_dbclick(self.toggle_unique)

        self.enc_params.register_cb_encoder(self._cb_param_enc)

    def __enter__(self):
        super().__enter__()
        self.set_bank(0)
        self.enc_nodes.set_value(0.3)
        self.enc_params.set_value(0)
        self.enc_nodes.set_indicator_brightness(self.indicator_brightness_off)

        self.enc_nodes.set_color(self.color_node_default)
        self.enc_params.set_color(self.color_param_default)
        self.enc_nodes[self.current_node].set_color(self.color_selected)

    def _cb_param_enc(self, encoder: Encoder, ts):
        param_idx = self.enc_params.get_idx(encoder)
        value = encoder.value
        self.data[self.current_node][param_idx] = value
        self.data[(*np.where(self.selected_for_copy), *param_idx)] = value

    def node_hold(self, node, tx):
        node_idx = self.enc_nodes.get_idx(node)

        if not self.sidebuttons[(0, *self.copy_param)].pressed:
            self.current_node = node_idx
            colors = np.empty(self.enc_nodes.shape, int)
            colors[:] = ft_colors.blue
            colors[node_idx] = self.color_selected
            self.enc_nodes.set_color(colors)
            self.enc_params.set_value(self.data[node_idx])
            self.selected_for_copy[:] = 0

        elif node_idx != self.current_node:
            self.selected_for_copy[node_idx] = 1
            node.set_color(self.color_copy)
            self.data[self.enc_nodes.get_idx(
                node)] = self.data[self.current_node]

    def toggle_onoff(self, node: Encoder, ts):
        self.noeds_on[self.enc_nodes.get_idx(node)] ^= 1
        if self.noeds_on[self.enc_nodes.get_idx(node)]:
            node.set_indicator_brightness(self.indicator_brightness_on)
        else:
            node.set_indicator_brightness(self.indicator_brightness_off)

    def toggle_unique(self, node: Encoder, ts):
        node.set_indicator_brightness(self.indicator_brightness_on)
        self.noeds_on[self.enc_nodes.get_idx(node)] = 1
        for _node in self.enc_nodes:
            if _node is not node:
                _node.set_indicator_brightness(self.indicator_brightness_off)
                self.noeds_on[self.enc_nodes.get_idx(_node)] = 0
