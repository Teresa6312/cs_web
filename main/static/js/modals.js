function isThere(param,id){
  if(param!=""){
    $("#"+id).attr('value', param);
  }
  else{
    $("#"+id).attr("value","");
  }
}//end of isThere


function submitForm(csrf, submit_url){
  let formpass=true;
  let inputs = document.forms["newAddressForm_js"].getElementsByTagName("input");
  for(var i = 0, a; a = inputs[i++];){
    if(a.required && a.value==''){
        a.style.background = "#ffb2b2";
        formpass=false;
    }
  }

  if(formpass){
      let addobject={'csrfmiddlewaretoken': csrf,
                      'addform':$('#newAddressForm_js').serialize(),
                      'is_popup':"True"};
      
      $.ajax({
        type: "POST",
        url: submit_url,
        data: addobject,
        success: function(data){
          $('#newAddressFormModalBody').append($(data).find('#newAddressFormModal').find('#newAddressForm'));
          $('#newAddressFormModal').append($(data).find('#newAddressFormModal').find('script'));

          if($(data).find('#newAddressFormModal').find('.messagelist').children().length == 0){
            $('#newAddressFormModal').modal('hide');
            $('#default_address_card').remove();
            $('#newAddressForm_js').remove();
            $('#default_address_block').append($(data).find('#default_address_card'));
          }
          else{
            $('#id_follow_user_infor_block').before($(data).find('.messagelist'));
            $('#.messagelist').hide().slideDown(500);
          }
        },
        failure: function(data){
          $('#id_follow_user_infor_block').before($(data).find('.messagelist'));
          $('#.messagelist').hide().slideDown(500);
        },
      });
    }
}//end of submitForm


function createAddForm(user,csrf, submit_url) {
    var addform = document.createElement("FORM");
    addform.setAttribute("id", "newAddressForm_js");

    var formblock = document.createElement("div");
    formblock.setAttribute("class", "w3-row");

    var fuiblock = document.createElement("div");
    fuiblock.setAttribute("id", "id_follow_user_infor_block");

    var fui = document.createElement("button");
    fui.setAttribute("type", "button");
    fui.setAttribute("id", "id_follow_user_infor");
    fui.append("Follow User Information");
    fui.innerHTML = 'Follow User Information';
    fui.onclick = function(){
      isThere(user.first_name,"id_first_name");
      isThere(user.last_name,"id_last_name");
      isThere(user.email,"id_email");
      isThere(user.phone,"id_phone");
    };

    fuiblock.appendChild(fui);
    formblock.appendChild(fuiblock);

    var fnblock = document.createElement("div");
    fnblock.setAttribute("class", "w3-half w3-container");
    fnblock.append('First Name:');

    var fn = document.createElement("INPUT");
    fn.setAttribute("id", "id_first_name");
    fn.setAttribute("type", "text");
    fn.setAttribute("name", "first_name");
    fn.setAttribute("class", "w3-input w3-border");
    fn.required = true;
    fnblock.appendChild(fn);
    formblock.appendChild(fnblock);

    var lnblock = document.createElement("div");
    lnblock.setAttribute("class", "w3-half w3-container");
    lnblock.append('Last Name:');

    var ln = document.createElement("INPUT");
    ln.setAttribute("id", "id_last_name");
    ln.setAttribute("type", "text");
    ln.setAttribute("name", "last_name");
    ln.setAttribute("class", "w3-input w3-border");
    ln.required = true;
    lnblock.appendChild(ln);
    formblock.appendChild(lnblock);


    var emblock = document.createElement("div");
    emblock.setAttribute("class", "w3-half w3-container");
    emblock.append('Email:');

    var em = document.createElement("INPUT");
    em.setAttribute("id", "id_email");
    em.setAttribute("type", "text");
    em.setAttribute("name", "email");
    em.setAttribute("class", "w3-input w3-border");
    emblock.appendChild(em);
    formblock.appendChild(emblock);


    var phblock = document.createElement("div");
    phblock.setAttribute("class", "w3-half w3-container");
    phblock.append('Phone:');

    var ph = document.createElement("INPUT");
    ph.setAttribute("id", "id_phone");
    ph.setAttribute("type", "text");
    ph.setAttribute("name", "phone");
    ph.setAttribute("class", "w3-input w3-border");
    phblock.appendChild(ph);
    formblock.appendChild(phblock);


    var adblock = document.createElement("div");
    adblock.setAttribute("class", " w3-container");

    adblock.append('Address:');
    var ad = document.createElement("INPUT");
    ad.setAttribute("id", "id_address");
    ad.setAttribute("type", "text");
    ad.setAttribute("name", "address");
    ad.setAttribute("class", "w3-input w3-border");
    ad.required = true;
    adblock.appendChild(ad);

    adblock.append('Apartment:');
    var ap = document.createElement("INPUT");
    ap.setAttribute("id", "id_apt");
    ap.setAttribute("type", "text");
    ap.setAttribute("name", "apt");
    ap.setAttribute("class", "w3-input w3-border");
    adblock.appendChild(ap);

    formblock.appendChild(adblock);


    var ctblock = document.createElement("div");
    ctblock.setAttribute("class", "w3-quarter w3-container");
    ctblock.append('City:');

    var ct = document.createElement("INPUT");
    ct.setAttribute("id", "id_city");
    ct.setAttribute("type", "text");
    ct.setAttribute("name", "city");
    ct.setAttribute("class", "w3-input w3-border");
    ct.required = true;
    ctblock.appendChild(ct);
    formblock.appendChild(ctblock);



    var stblock = document.createElement("div");
    stblock.setAttribute("class", "w3-quarter w3-container");
    stblock.append('State:');

    var st = document.createElement("INPUT");
    st.setAttribute("id", "id_state");
    st.setAttribute("type", "text");
    st.setAttribute("name", "state");
    st.setAttribute("class", "w3-input w3-border");
    st.required = true;
    stblock.appendChild(st);
    formblock.appendChild(stblock);


    var coblock = document.createElement("div");
    coblock.setAttribute("class", "w3-quarter w3-container");
    coblock.append('Country:');

    var co = document.createElement("INPUT");
    co.setAttribute("id", "id_country");
    co.setAttribute("type", "text");
    co.setAttribute("name", "country");
    co.setAttribute("class", "w3-input w3-border");
    co.required = true;
    coblock.appendChild(co);
    formblock.appendChild(coblock);

    var zpblock = document.createElement("div");
    zpblock.setAttribute("class", "w3-quarter w3-container");
    zpblock.append('Zip Code:');

    var zp = document.createElement("INPUT");
    zp.setAttribute("id", "id_zipcode");
    zp.setAttribute("type", "text");
    zp.setAttribute("name", "zipcode");
    zp.setAttribute("class", "w3-input w3-border");
    zp.required = true;
    zpblock.appendChild(zp);
    formblock.appendChild(zpblock);

    var sv = document.createElement("button");
    sv.setAttribute("type", "button");
    sv.setAttribute("id", "newAddressSubmitBtn");
    sv.setAttribute("onclick", "submitForm()");
    sv.innerHTML = 'Save';
    sv.onclick = function(){
      submitForm(csrf, submit_url);
    };
    formblock.appendChild(sv);

    var ca = document.createElement("button");
    ca.setAttribute("type", "button");
    ca.setAttribute("id", "close");
    ca.setAttribute("data-dismiss", "modal");
    ca.setAttribute("aria-label", "Close");
    ca.innerHTML = 'Cancel';
    formblock.appendChild(ca);

    addform.appendChild(formblock);
    if($('#newAddressForm_js').length==0){
        $('#newAddressFormModalBody').append(addform);
   }
   $('#newAddressFormModal').modal('show');

}//end of create address form
