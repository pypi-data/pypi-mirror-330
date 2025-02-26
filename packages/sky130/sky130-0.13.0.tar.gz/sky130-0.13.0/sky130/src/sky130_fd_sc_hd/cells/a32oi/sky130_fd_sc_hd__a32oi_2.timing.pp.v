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


`ifndef SKY130_FD_SC_HD__A32OI_2_TIMING_PP_V
`define SKY130_FD_SC_HD__A32OI_2_TIMING_PP_V

/**
 * a32oi: 3-input AND into first input, and 2-input AND into
 *        2nd input of 2-input NOR.
 *
 *        Y = !((A1 & A2 & A3) | (B1 & B2))
 *
 * Verilog simulation timing model.
 */

`timescale 1ns / 1ps
`default_nettype none

// Import user defined primitives.
`include "../../models/udp_pwrgood_pp_pg/sky130_fd_sc_hd__udp_pwrgood_pp_pg.v"

`celldefine
module sky130_fd_sc_hd__a32oi_2 (
    Y   ,
    A1  ,
    A2  ,
    A3  ,
    B1  ,
    B2  ,
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
    input  B2  ;
    input  VPWR;
    input  VGND;
    input  VPB ;
    input  VNB ;

    // Local signals
    wire nand0_out        ;
    wire nand1_out        ;
    wire and0_out_Y       ;
    wire pwrgood_pp0_out_Y;

    //                                 Name         Output             Other arguments
    nand                               nand0       (nand0_out        , A2, A1, A3            );
    nand                               nand1       (nand1_out        , B2, B1                );
    and                                and0        (and0_out_Y       , nand0_out, nand1_out  );
    sky130_fd_sc_hd__udp_pwrgood_pp$PG pwrgood_pp0 (pwrgood_pp0_out_Y, and0_out_Y, VPWR, VGND);
    buf                                buf0        (Y                , pwrgood_pp0_out_Y     );

specify
if ((A2&A3&!B1&!B2)) (A1 -=> Y) = (0:0:0,0:0:0);
if ((A2&A3&!B1&B2)) (A1 -=> Y) = (0:0:0,0:0:0);
if ((A2&A3&B1&!B2)) (A1 -=> Y) = (0:0:0,0:0:0);
if ((A1&A3&!B1&!B2)) (A2 -=> Y) = (0:0:0,0:0:0);
if ((A1&A3&!B1&B2)) (A2 -=> Y) = (0:0:0,0:0:0);
if ((A1&A3&B1&!B2)) (A2 -=> Y) = (0:0:0,0:0:0);
if ((A1&A2&!B1&!B2)) (A3 -=> Y) = (0:0:0,0:0:0);
if ((A1&A2&!B1&B2)) (A3 -=> Y) = (0:0:0,0:0:0);
if ((A1&A2&B1&!B2)) (A3 -=> Y) = (0:0:0,0:0:0);
if ((!A1&!A2&!A3&B2)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((!A1&!A2&A3&B2)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((!A1&A2&!A3&B2)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((!A1&A2&A3&B2)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((A1&!A2&!A3&B2)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((A1&!A2&A3&B2)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((A1&A2&!A3&B2)) (B1 -=> Y) = (0:0:0,0:0:0);
if ((!A1&!A2&!A3&B1)) (B2 -=> Y) = (0:0:0,0:0:0);
if ((!A1&!A2&A3&B1)) (B2 -=> Y) = (0:0:0,0:0:0);
if ((!A1&A2&!A3&B1)) (B2 -=> Y) = (0:0:0,0:0:0);
if ((!A1&A2&A3&B1)) (B2 -=> Y) = (0:0:0,0:0:0);
if ((A1&!A2&!A3&B1)) (B2 -=> Y) = (0:0:0,0:0:0);
if ((A1&!A2&A3&B1)) (B2 -=> Y) = (0:0:0,0:0:0);
if ((A1&A2&!A3&B1)) (B2 -=> Y) = (0:0:0,0:0:0);
endspecify
endmodule
`endcelldefine

`default_nettype wire
`endif  // SKY130_FD_SC_HD__A32OI_2_TIMING_PP_V
