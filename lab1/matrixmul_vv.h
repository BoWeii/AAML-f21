// matrixmul_vv vd, vs2, vs1
// .word 0xe2824057
MATRIX_MUL({
  int run = (i / 4);
  int tmp = i - (4 * run);
  for (reg_t times = 0; times < 4; ++times)
  {
    auto &vd = P.VU.elt<type_sew_t<e32>::type>(rd_num, i, true);        //ok
    auto x = P.VU.elt<type_sew_t<e32>::type>(rs1_num, 4 * run + times); //ok
    auto y = P.VU.elt<type_sew_t<e32>::type>(rs2_num, tmp + 4 * times);
    vd = x * y + vd;
  }
})