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

`ifndef SKY130_FD_SC_HD__SDFSBP_PP_SYMBOL_V
`define SKY130_FD_SC_HD__SDFSBP_PP_SYMBOL_V

/**
 * sdfsbp: Scan delay flop, inverted set, non-inverted clock,
 *         complementary outputs.
 *
 * Verilog stub (with power pins) for graphical symbol definition
 * generation.
 *
 * WARNING: This file is autogenerated, do not modify directly!
 */

`timescale 1ns / 1ps
`default_nettype none

(* blackbox *)
module sky130_fd_sc_hd__sdfsbp (
    //# {{data|Data Signals}}
    input  D    ,
    output Q    ,
    output Q_N  ,

    //# {{control|Control Signals}}
    input  SET_B,

    //# {{scanchain|Scan Chain}}
    input  SCD  ,
    input  SCE  ,

    //# {{clocks|Clocking}}
    input  CLK  ,

    //# {{power|Power}}
    input  VPB  ,
    input  VPWR ,
    input  VGND ,
    input  VNB
);
endmodule

`default_nettype wire
`endif  // SKY130_FD_SC_HD__SDFSBP_PP_SYMBOL_V
