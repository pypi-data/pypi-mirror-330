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


`ifndef SKY130_FD_SC_HD__NOR3_4_FUNCTIONAL_V
`define SKY130_FD_SC_HD__NOR3_4_FUNCTIONAL_V

/**
 * nor3: 3-input NOR.
 *
 *       Y = !(A | B | C | !D)
 *
 * Verilog simulation functional model.
 */

`timescale 1ns / 1ps
`default_nettype none

`celldefine
module sky130_fd_sc_hd__nor3_4 (
    Y,
    A,
    B,
    C
);

    // Module ports
    output Y;
    input  A;
    input  B;
    input  C;

    // Local signals
    wire nor0_out_Y;

    //  Name  Output      Other arguments
    nor nor0 (nor0_out_Y, C, A, B        );
    buf buf0 (Y         , nor0_out_Y     );

endmodule
`endcelldefine

`default_nettype wire
`endif  // SKY130_FD_SC_HD__NOR3_4_FUNCTIONAL_V
