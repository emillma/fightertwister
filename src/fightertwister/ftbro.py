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

        self.color_node_selected = ft_colors.green
        self.color_copy = ft_colors.yellow
        self.color_node_default = ft_colors.blue
        self.color_param_default = ft_colors.magenta

        self.enc_selectors = self.encoders[0, :2, :]
        self.enc_nodes = self.enc_selectors[:, :3]
        self.enc_mic = self.encoders[0, 1, 3]
        self.enc_main_volume = self.encoders[0, 1, 3]
        self.enc_params = self.encoders[0, 2:, :]

        self.button_copy = self.sidebuttons[0, 2, 0]

        self.data = np.zeros(
            (*self.enc_selectors.shape, *self.enc_params.shape))
        self.current_node = (0, 0)

        self.nodes_on = np.zeros(self.enc_selectors.shape, int)
        self.selected_for_copy = np.zeros(self.enc_selectors.shape, int)

        self.enc_selectors.set_delay_hold(200)

        self.enc_selectors.register_cb_hold(self._selector_select)
        self.enc_selectors.register_cb_click(self._toggle_onoff)

        self.enc_params.register_cb_encoder(self._param_enc)

        self.enc_nodes.register_cb_hold(self._enable_copy)
        self.enc_nodes.register_cb_dbclick(self._toggle_unique)

        self.enc_mic.register_cb_hold(self._selector_select)

        self.button_copy.register_cb_dbclick(self._all_enable_copy)
        self.button_copy.register_cb_click(self._all_disable_copy)

    def __enter__(self):
        super().__enter__()
        self.set_bank(0)
        self.enc_selectors.set_value(0.3)
        self.enc_params.set_value(0)
        self.enc_selectors.set_indicator_brightness(
            self.indicator_brightness_off)

        self.enc_selectors.set_color(self.color_node_default)
        self.enc_params.set_color(self.color_param_default)
        self.enc_selectors[self.current_node].set_color(
            self.color_node_selected)

    def _param_enc(self, encoder: Encoder, ts):
        param_idx = self.enc_params.get_idx(encoder)
        value = encoder.value
        self.data[self.current_node][param_idx] = value
        self.data[(*np.where(self.selected_for_copy), *param_idx)] = value

    def _selector_select(self, enc, ts):
        enc_idx = self.enc_selectors.get_idx(enc)
        if not self.button_copy.pressed:
            self.current_node = enc_idx
            colors = np.empty(self.enc_selectors.shape, int)
            colors[:] = self.color_node_default
            colors[enc_idx] = self.color_node_selected
            self.enc_selectors.set_color(colors)
            self.enc_params.set_value(self.data[enc_idx])
            self.selected_for_copy[:] = 0

    def _enable_copy(self, node: Encoder, ts):
        node_idx = self.enc_selectors.get_idx(node)
        if node_idx != self.current_node and self.button_copy.pressed:
            self.selected_for_copy[node_idx] = 1
            node.set_color(self.color_copy)
            self.data[self.enc_selectors.get_idx(
                node)] = self.data[self.current_node]

    def _all_enable_copy(self, button: Button, ts):
        for node in self.enc_nodes:
            self._enable_copy(node, ts)

    def _all_disable_copy(self, button: Button, ts):
        for node in self.enc_selectors[np.where(self.selected_for_copy)]:
            node.set_color(self.color_node_default)
        self.selected_for_copy[:] = 0

    def _toggle_onoff(self, node: Encoder, ts):
        self.nodes_on[self.enc_selectors.get_idx(node)] ^= 1
        if self.nodes_on[self.enc_selectors.get_idx(node)]:
            node.set_indicator_brightness(self.indicator_brightness_on)
        else:
            node.set_indicator_brightness(self.indicator_brightness_off)

    def _toggle_unique(self, node: Encoder, ts):
        node.set_indicator_brightness(self.indicator_brightness_on)
        self.nodes_on[self.enc_selectors.get_idx(node)] = 1
        for _node in self.enc_nodes:
            if _node is not node:
                _node.set_indicator_brightness(self.indicator_brightness_off)
                self.nodes_on[self.enc_selectors.get_idx(_node)] = 0
