import numpy as np
from .fightertwister import FighterTwister
from .encoder import Encoder
from .button import Button
from .utils import ft_colors
from .ftcollections import EncoderCollection


class FtBro(FighterTwister):
    def __init__(self):
        super().__init__()

        self.enc_selectors = self.encoders[0, :2, :]
        self.enc_nodes = self.enc_selectors[:, :3]
        self.enc_main_volume = self.enc_selectors[0, 3]
        self.enc_mic = self.enc_selectors[1, 3]
        self.enc_params = self.encoders[0, 2:, :]

        self.button_params = self.sidebuttons[0:2, 0, 0]
        self.button_inspect = self.sidebuttons[0:2, 1, 0]
        self.button_copy = self.sidebuttons[0, 2, 0]

        self.color_node_selected = ft_colors.cyan
        self.color_copy = ft_colors.yellow
        self.color_node_default = ft_colors.blue
        self.color_param_default = ft_colors.green
        self.color_main_volume = ft_colors.orange
        self.color_mic = ft_colors.magenta

        self.colors_selector_default = np.zeros(self.enc_selectors.shape, int)
        self.colors_selector_default[:] = self.color_node_default
        self.colors_selector_default[0, 3] = self.color_main_volume
        self.colors_selector_default[1, 3] = self.color_mic

        self.data = np.zeros(
            (*self.enc_selectors.shape, *self.enc_params.shape))
        self.current_node = (0, 0)

        self.selected_node = self.enc_selectors[0, 0]
        self.active_nodes = EncoderCollection(self.selected_node)

        self.encoders.set_extra_values(
            np.zeros(self.enc_params.shape), _broadcast=False)

        self.nodes_on = np.zeros(self.enc_selectors.shape, int)
        self.selected_for_copy = np.zeros(self.enc_selectors.shape, int)

        self.enc_selectors.set_delay_hold(200)

        self.enc_selectors.register_cb_hold(self.node_hold)
        self.enc_selectors.register_cb_click(self.toggle_onoff)

        self.enc_params.register_cb_encoder(self._param_enc)

        self.enc_nodes.register_cb_hold(self.togle_copy_mode)
        # self.enc_nodes.register_cb_dbclick(self._toggle_unique)

        # self.enc_mic.register_cb_hold(self._selector_select)

        self.button_copy.register_cb_dbclick(self.enable_all_copy)
        self.button_copy.register_cb_click(self.disable_all_copy)

        self.button_params.register_cb_click(lambda *_: self.set_bank(0))
        self.button_inspect.register_cb_click(lambda *_: self.set_bank(1))

    def __enter__(self):
        super().__enter__()
        self.set_bank(0)
        self.enc_selectors.set_value(0.3)
        self.enc_selectors.set_on_off(0)
        self.enc_params.set_value(0)
        self.enc_selectors.set_color(self.colors_selector_default)
        self.enc_selectors[self.current_node].set_color(
            self.color_node_selected)
        self.enc_params.set_color(self.color_param_default)

    def _param_enc(self, encoder: Encoder, ts):
        self.active_nodes.set_extra_values(self.enc_params._value,
                                           _broadcast=False)

    def node_hold(self, node: Encoder, ts):
        if not self.button_copy.pressed:
            self.active_nodes.set_color(self.color_node_default)
            self.selected_node = node
            self.selected_node.set_color(self.color_node_selected)
            self.active_nodes = EncoderCollection(self.selected_node)
            self.enc_params.set_value(node.extra_values)

    def togle_copy_mode(self, node: Encoder, ts):
        if node is not self.selected_node and self.button_copy.pressed:
            if node not in self.active_nodes:
                self.active_nodes = EncoderCollection(
                    [enc for enc in self.active_nodes] + [node])
                node.set_color(self.color_copy)
                node.set_extra_values(self.selected_node.extra_values)
            else:
                self.active_nodes = EncoderCollection(
                    [enc for enc in self.active_nodes if enc is not node])
                node.set_color(self.color_node_default)

    def enable_all_copy(self, button: Button, ts):
        self.active_nodes = self.enc_nodes
        [node.set_color(self.color_copy) for node in self.active_nodes
         if node is not self.selected_node]

    def disable_all_copy(self, button: Button, ts):
        [node.set_color(self.color_node_default) for node in self.active_nodes
         if node is not self.selected_node]
        self.active_nodes = EncoderCollection(self.selected_node)

    def toggle_onoff(self, node: Encoder, ts):
        on = node.on ^ 1
        node.set_on_off(on)
