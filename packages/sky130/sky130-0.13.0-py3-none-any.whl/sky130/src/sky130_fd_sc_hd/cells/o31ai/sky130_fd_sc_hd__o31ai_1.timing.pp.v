/*
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


`ifndef SKY130_FD_SC_HD__O31AI_1_TIMING_PP_V
`define SKY130_FD_SC_HD__O31AI_1_TIMING_PP_V

/**
 * o31ai: 3-input OR into 2-input NAND.
 *
 *        Y = !((A1 | A2 | A3) & B1)
 *
 * Verilog simulation timing model.
 */

`timescale 1ns / 1ps
`default_nettype none

// Import user defined primitives.
`include "../../models/udp_pwrgood_pp_pg/sky130_fd_sc_hd__udp_pwrgood_pp_pg.v"

`celldefine
module sky130_fd_sc_hd__o31ai_1 (
    Y   ,
    A1  ,
    A2  ,
    A3  ,
    B1  ,
    VPWR,
    VGND,
    VPB ,
    VNB
);

    // Module ports
    output Y   ;
    input  A1  ;
    input  A2  ;
    input  A3  ;
    input  B1  ;
    input  VPWR;
    input  VGND;
    input  VPB ;
    input  VNB ;

    // Local signals
    wire or0_out          ;
    wire nand0_out_Y      ;
    wire pwrgood_pp0_out_Y;

    //                                 Name         Output             Other arguments
    or                                 or0         (or0_out          , A2, A1, A3             );
    nand                               nand0       (nand0_out_Y      , B1, or0_out            );
    sky130_fd_sc_hd__udp_pwrgood_pp$PG pwrgood_pp0 (pwrgood_pp0_out_Y, nand0_out_Y, VPWR, VGND);
    buf                                buf0        (Y                , pwrgood_pp0_out_Y      );

specify
(A1 -=> Y) = (0:0:0,0:0:0);
(A2 -=> Y) = (0:0:0,0:0:0);
(A3 -=> Y) = (0:0:0,0:0:0);
if ((!A1&!A2&A3)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((!A1&A2&!A3)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((!A1&A2&A3)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((A1&!A2&!A3)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((A1&!A2&A3)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((A1&A2&!A3)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((A1&A2&A3)) (B1 -=> Y) = (0:0:0,0:0:0);
endspecify
endmodule
`endcelldefine

`default_nettype wire
`endif  // SKY130_FD_SC_HD__O31AI_1_TIMING_PP_V
