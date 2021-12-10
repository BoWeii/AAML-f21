`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/01/2021 02:09:54 PM
// Design Name: 
// Module Name: PE
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module PE(clk,reset_n,enable,down_o,right_o,left_i,weight,up_i);

input clk,reset_n,enable;
output reg[15:0]down_o;
output reg[15:0]right_o;
input [7:0]weight;
input [7:0]left_i;
input [15:0]up_i;

always@(posedge clk) begin

    if (~enable) begin
        down_o <= 16'b0;
        right_o <= 8'b0;
    end
    else begin
        down_o <= weight * left_i + up_i;
        right_o <= left_i;
    end

end

endmodule

