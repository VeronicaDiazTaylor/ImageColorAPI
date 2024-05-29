const INDEX_BASE_COLOR = 0
const INDEX_COLOR_PALLET = 1
const INDEX_NEAREST_COLOR = 2

let select = document.getElementById('process');
if (select instanceof Element) {
    select.onchange = event => {
        ['base_pallet', 'n_clusters'].forEach( it => {
            let added_select = document.getElementById(it);
            if (added_select != null) {
                added_select.remove();
            }
        });

        switch (select.selectedIndex) {
            case INDEX_COLOR_PALLET:
                select.after(getNClustersElement());
                break;

            case INDEX_NEAREST_COLOR:
                select.after(getBasePalletElement());
                break;
        }
    }
}

function getNClustersElement() {
    let node = document.createElement('select');
    node.id = 'n_clusters';
    node.name = 'n_clusters';
    for (let i = 3; i < 7; i++) {
        let opt = document.createElement('option');
        opt.value = i.toString();
        opt.text = i.toString();
        node.add(opt);
    }
    return node;
}

function getBasePalletElement() {
    let node = document.createElement('select');
    node.id = 'base_pallet';
    node.name = 'base_pallet';
    let jis_opt = document.createElement('option');
    jis_opt.value = 'j';
    jis_opt.text = 'JIS色鉛筆45種';
    let d_opt = document.createElement('option');
    d_opt.value = 'd';
    d_opt.text = '原色140種';
    let w_opt = document.createElement('option');
    w_opt.value = 'w';
    w_opt.text = '和色465種';
    let y_opt = document.createElement('option');
    y_opt.value = 'y';
    y_opt.text = '洋色285種';
    node.add(jis_opt);
    node.add(d_opt);
    node.add(w_opt);
    node.add(y_opt);
    return node;
}