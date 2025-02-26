/**
 * Copyright 2020 The SkyWater PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

`ifndef SKY130_FD_SC_HD__UDP_DLATCH_P_PP_PG_N_SYMBOL_V
`define SKY130_FD_SC_HD__UDP_DLATCH_P_PP_PG_N_SYMBOL_V

/**
 * udp_dlatch$P_pp$PG$N: D-latch, gated standard drive / active high
 *                       (Q output UDP)
 *
 * Verilog stub (with power pins) for graphical symbol definition
 * generation.
 *
 * WARNING: This file is autogenerated, do not modify directly!
 */

`timescale 1ns / 1ps
`default_nettype none

(* blackbox *)
module sky130_fd_sc_hd__udp_dlatch$P_pp$PG$N (
    //# {{data|Data Signals}}
    input  D       ,
    output Q       ,

    //# {{clocks|Clocking}}
    input  GATE    ,

    //# {{power|Power}}
    input  NOTIFIER,
    input  VPWR    ,
    input  VGND
);
endmodule

`default_nettype wire
`endif  // SKY130_FD_SC_HD__UDP_DLATCH_P_PP_PG_N_SYMBOL_V
