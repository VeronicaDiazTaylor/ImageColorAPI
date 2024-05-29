let select = document.getElementById('process') ?? false;
if (select instanceof Element) {
    select.onchange = event => {
        if (select.selectedIndex === 2) {
            let added_select = document.getElementById('base_pallet')
            if (added_select == null) {
                let node = document.createElement('select')
                node.id = 'base_pallet'
                node.name = 'base_pallet'
                let jis_opt = document.createElement('option')
                jis_opt.value = 'j'
                jis_opt.text = 'JIS色鉛筆45種'
                let d_opt = document.createElement('option')
                d_opt.value = 'd'
                d_opt.text = '原色140種'
                let w_opt = document.createElement('option')
                w_opt.value = 'w'
                w_opt.text = '和色465種'
                node.add(jis_opt)
                node.add(d_opt)
                node.add(w_opt)
                select.after(node);
            }
        } else {
            let added_select = document.getElementById('base_pallet')
            if (added_select != null) {
                added_select.remove()
            }
        }
    }
}
