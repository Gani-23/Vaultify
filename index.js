/**
 * Created by fipso on 13.10.16.
 */
var CryptoJS = require("crypto-js");

var CryptoJSAesJson = {
    stringify: function (cipherParams) {
        var j = {ct: cipherParams.ciphertext.toString(CryptoJS.enc.Base64)};
        if (cipherParams.iv) j.iv = cipherParams.iv.toString();
        if (cipherParams.salt) j.s = cipherParams.salt.toString();
        return JSON.stringify(j);
    },
    parse: function (jsonStr) {
        var j = JSON.parse(jsonStr);
        var cipherParams = CryptoJS.lib.CipherParams.create({ciphertext: CryptoJS.enc.Base64.parse(j.ct)});
        if (j.iv) cipherParams.iv = CryptoJS.enc.Hex.parse(j.iv);
        if (j.s) cipherParams.salt = CryptoJS.enc.Hex.parse(j.s);
        return cipherParams;
    }
};


module.exports = {

    build: function (score, url) {

        var timestamp = new Date().getTime();
        var hash = CryptoJS.AES.encrypt(JSON.stringify({score: score, timestamp: timestamp}), "crmjbjm3lczhlgnek9uaxz2l9svlfjw14npauhen", { format:
        CryptoJSAesJson}).toString();
        var sData = JSON.stringify({
            score: score,
            url: "/game/" + url,
            play_time: 20,
            hash: hash
        });

        return sData;

    }
};