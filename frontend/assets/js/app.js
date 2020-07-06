let headers = {
    'Content-Type': 'application/json'
}

if (localStorage.getItem("rsswatcher-jwt-token")) {
    headers["X-Access-Token"] = localStorage.getItem("rsswatcher-jwt-token")
}

const instance = axios.create({
    baseURL: 'http://localhost:5000/',
    headers
});

$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

$("#loginForm").submit(function (e) {
    e.preventDefault();
    let el = $(this);
    let data = el.serializeObject();
    console.log(data)
    el.find('.btn-login').prop('disabled', true);
    instance.post("/login", data)
        .then(function (response) {
            el.find('.btn-login').prop('disabled', false);
            location.href = 'feeds.html';
            localStorage.setItem("rsswatcher-jwt-token", response.data.jwt_token);
        })
        .catch(function (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.response.data.message
            });
            el.find('.btn-login').prop('disabled', false);
        });
});

function logout() {
    instance.delete("/login")
        .then(function (response) {
            localStorage.clear();
            location.href = "index.html";
        })
        .catch(function (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.response.data.message
            });
            el.find('.btn-login').prop('disabled', false);
        });
}

function readDetails(el) {
    let data = JSON.parse(decodeURIComponent($(el).data("row")));
    $('#detailsModalLabel').text(data.header);
    $('#detailsModal .modal-body').html(data.detail);
    $('#detailsModal .modal-footer').html(`
        <div>${moment(data.date).format('YYYY-MM-DD HH:mm:ss')}</div>
        ${getRank(data.id, data.rank)}
    `);
    $('#detailsModal').modal('show')
}

function getRank(id, data) {
    let rank = "";
    let rate = 1;
    for (let i = 0; i < data; i++) {
        rank += `<i class="fa fa-star" onclick="setRank('${id}', '${rate}', '${data}')" style="cursor: pointer; padding: 0 1px;"></i>`;
        rate++;
    }
    for (let i = 0; i < 5 - data; i++) {
        rank += `<i class="fa fa-star-o" onclick="setRank('${id}', '${rate}')" style="cursor: pointer; padding: 0 1px;"></i>`;
        rate++;
    }
    return `<div class="modal-rank-${id}">${rank}</div>`;
}

function setRank(id, rate, current = null) {
    if (rate == 1 && rate == current) {
        rate = 0;
    }
    instance.put("/feeds/" + id, {
        rank: parseFloat(rate)
    })
        .then(function (response) {
            $(`.modal-rank-${id}`).html(getRank(id, rate));
            let data = JSON.parse(decodeURIComponent($("#rowButton" + id).data("row")));
            data.rank = rate;
            $("#rowButton" + id).data("row", encodeURIComponent(JSON.stringify(data)));
        })
        .catch(function (error) {
        });
}