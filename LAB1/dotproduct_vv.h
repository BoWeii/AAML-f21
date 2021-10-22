// dotproduct_vv vd, vs2, vs1
// .word 0xe2443057 (2-b)
VI_VV_LOOP({
  vd = vs2 * vs1;
})

auto &res = P.VU.elt<type_sew_t<e32>::type>(rd_num, P.VU.vstart->read(), true);

for (reg_t i = P.VU.vstart->read(); i < vl; ++i)
{
  if(i==0) continue;
  auto &temp = P.VU.elt<type_sew_t<e32>::type>(rd_num, i, true);
  res += temp;
  temp = 0;
}