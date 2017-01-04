module oneshot (
    input        clk,
    input  [1:0] edge_sig,
    output [1:0] level_sig
);

reg [1:0] cur_value;
reg [1:0] last_value;

assign level_sig = ~cur_value & last_value; // falling edge detection

always @( posedge clk ) begin
    cur_value <= edge_sig;
    last_value <= cur_value;
end

endmodule
