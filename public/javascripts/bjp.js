jQuery().ready(function() {
 
  jQuery.validator.addMethod("phoneNumber", function (phone_number, element) {
    return this.optional(element) || phone_number.match(/^[0-9]{2}[\s-.]*[0-9]{2}[\s-.]*[0-9]{2}[\s-.]*[0-9]{2}[\s-.]*[0-9]{2}[\s-.]*$/);
  }, "Please specify a valid phone number");

  var v = jQuery("#basicform").validate({
      rules: {
        uname: {
          required: true,
          minlength: 2,
          maxlength: 30
        },
        umanager: {
          required: true,
          minlength: 2,
          maxlength: 30
        },
        cname: {
          required: true,
          minlength: 2,
          maxlength: 50,
        },
        ccontactname: {
          required: true,
          minlength: 2,
          maxlength: 100,
        },
        ccontacttel: {
          required: true,
          minlength: 10,
          maxlength: 14,
          phoneNumber: true
        },
        missionname: {
          required: true,
          minlength: 2,
          maxlength: 100,
        },
        missioncode: {
          required: true,
          minlength: 2,
          maxlength: 100,
        },
        missionnature: {
          required: true,
          minlength: 2,
          maxlength: 100,
        },
 
      },
      errorElement: "span",
      errorClass: "help-inline-error",
      onkeyup: function(element) { $(element).valid(); },
      onfocusout: function(element) { $(element).valid(); },
    });
 
 
  // Binding next button on first step
  $(".open1").click(function() {
      if (v.form()) {
        $(".frm").hide("fast");
        $("#sf2").show("slow");
      }
   });
 
   // Binding next button on second step
   $(".open2").click(function() {
      if (v.form()) {
        $(".frm").hide("fast");
        $("#sf3").show("slow");
      }
    });
 
     // Binding back button on second step
    $(".back2").click(function() {
      $(".frm").hide("fast");
      $("#sf1").show("slow");
    });
 
     // Binding back button on third step
     $(".back3").click(function() {
      $(".frm").hide("fast");
      $("#sf2").show("slow");
    });
 
    $(".open3").click(function() {
      if (v.form()) {
        // optional
        // used delay form submission for a seccond and show a loader image
        $("#loader").show();
         setTimeout(function(){
           $("#basicform").html('<h2>Thanks for your time.</h2>');
         }, 1000);
        // Remove this if you are not using ajax method for submitting values
        return false;
      }
    });
});
