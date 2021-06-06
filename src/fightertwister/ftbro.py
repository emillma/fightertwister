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
        self.nodes = self.enc_selectors[:, :3]
        self.enc_main_volume = self.enc_selectors[0, 3]
        self.enc_mic = self.enc_selectors[1, 3]
        self.enc_params = self.encoders[0, 2:, :]

        for node in self.enc_selectors:
            params = EncoderCollection((2, 4), self)
            params.set_color(ft_colors.green)
            node.set_property('params', params)
            if node in self.nodes:
                params.register_cb_encoder(self.param_change)

        self.nodes.set_default_color(ft_colors.blue)

        self.enc_main_volume.register_cb_hold(self.volume_or_mic_hold)
        self.enc_main_volume.set_default_color(ft_colors.orange)

        self.enc_mic.register_cb_hold(self.volume_or_mic_hold)
        self.enc_mic.set_default_color(ft_colors.magenta)

        self.button_params = self.sidebuttons[0:2, 0, 0]
        self.button_inspect = self.sidebuttons[0:2, 1, 0]
        self.button_copy = self.sidebuttons[0, 2, 0]

        self.color_node_selected = ft_colors.cyan
        self.color_copy = ft_colors.yellow
        self.color_param_default = ft_colors.green
        self.color_main_volume = ft_colors.orange
        self.color_mic = ft_colors.magenta

        self.selected_node = self.enc_selectors[0, 0]
        self.encoder_slots[0, 2:] = self.selected_node.get_property('params')
        self.active_nodes = EncoderCollection(self.selected_node)

        for i in self.nodes:
            i.set_extra_values(np.zeros(self.enc_params.shape))

        # self.nodes_on = np.zeros(self.enc_selectors.shape, int)
        # self.selected_for_copy = np.zeros(self.enc_selectors.shape, int)

        self.nodes.register_cb_hold(self.node_hold)
        # self.enc_selectors.register_cb_click(self.toggle_onoff)

        # self.enc_params.register_cb_encoder(self._param_enc)

        self.nodes.register_cb_press(self.togle_copy_mode)
        # self.enc_nodes.register_cb_dbclick(self.toggle_solo)

        # # self.enc_mic.register_cb_hold(self._selector_select)

        self.button_copy.register_cb_dbclick(self.enable_all_copy)
        self.button_copy.register_cb_click(self.disable_all_copy)

        # self.button_params.register_cb_press(lambda *_: self.set_bank(0))
        # self.button_inspect.register_cb_press(lambda *_: self.set_bank(1))

    def __enter__(self):
        super().__enter__()
        self.set_bank(0)
        # self.encoders.set_follow_value(False)
        self.encoders.set_value(0.3)
        self.enc_selectors.set_on_off(1)
        self.enc_params.set_value(0)
        self.enc_selectors.set_color(self.enc_selectors.default_color)
        self.selected_node.set_color(self.color_node_selected)
        self.enc_params.set_color(self.color_param_default)

    def param_change(self, _node: Encoder, _ts):
        for node in filter(lambda node: node is not self.selected_node,
                           self.active_nodes):
            node.get_property('params').set_value(
                self.selected_node.get_property('params').value)

    def volume_or_mic_hold(self, node: Encoder, _ts):
        self.enc_selectors.set_color(
            self.enc_selectors.default_color)
        node.set_color(self.color_node_selected)
        self.encoder_slots[0, 2:] = node.get_property('params')
        self.selected_node = node
        self.active_nodes = EncoderCollection([])

    def node_hold(self, node: Encoder, _ts):
        if self.button_copy.pressed or node is self.selected_node:
            return
        self.enc_selectors.set_color(
            self.enc_selectors.default_color)
        self.selected_node = node
        self.selected_node.set_color(self.color_node_selected)
        self.encoder_slots[0, 2:] = node.get_property('params')
        self.active_nodes = EncoderCollection(self.selected_node)

    def togle_copy_mode(self, node: Encoder, ts):
        if node is not self.selected_node and self.button_copy.pressed:
            if node not in self.active_nodes:
                self.active_nodes = EncoderCollection(
                    [*self.active_nodes, node])
                node.set_color(self.color_copy)
                node.get_property('params').set_value(
                    self.selected_node.get_property('params').value)
            else:
                self.active_nodes = EncoderCollection(
                    [enc for enc in self.active_nodes if enc is not node])
                node.set_color(node.default_color)

    def enable_all_copy(self, button: Button, ts):
        self.active_nodes = self.nodes
        for node in filter(lambda node: node is not self.selected_node,
                           self.active_nodes):
            node.set_color(self.color_copy)
            node.get_property('params').set_value(
                self.selected_node.get_property('params').value)

    def disable_all_copy(self, button: Button, ts):
        [node.set_color(node.default_color)
         for node in self.active_nodes if node is not self.selected_node]
        self.active_nodes = EncoderCollection(self.selected_node)

    def toggle_onoff(self, node: Encoder, ts):
        if not self.button_copy.pressed:
            on_off = node.on ^ 1
            node.set_on_off(on_off)

    def toggle_solo(self, node: Encoder, ts):
        node.set_on_off(1)
        [i.set_on_off(0) for i in self.nodes if i is not node]
