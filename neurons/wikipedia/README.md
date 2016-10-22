# wikipedia

## Synopsis

Get the summary of a Wikipedia page.

## Options

| parameter | required | default | choices                     | comment                                                                                                                           |
|-----------|----------|---------|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| language  | yes      |         | E.g: "fr", "en", "it", "es" | See the list of available language in the "Note" section                                                                          |
| query     | yes      |         |                             | The wikipedia page you are looking for.  This parameter can be passed as an argument in the neuron from the order with {{ query}} |
| sentences | no       | 10      | Integer in range 1-10       | if set, return the first number of sentences(can be no greater than 10) specified in this parameter.                              |


## Return Values

| Name       | Description                             | Type   | sample                                                                                                                              |
|------------|-----------------------------------------|--------|-------------------------------------------------------------------------------------------------------------------------------------|
| summary    | Plain text summary of the searched page | string |  Wikipedia is a collaboratively edited, multilingual, free Internet encyclopedia supported by the non-profit Wikimedia Foundation.. |
| returncode | Error code. See bellow                  | string | SummaryFound                                                                                                                        |
| may_refer  | List of pages that can refer the query  | list   | ['Marc Le Bot', 'Bot', 'Jean-Marc Bot', 'bot', 'pied bot', 'robot', 'Sam Bot', 'Famille Both', 'Yves Bot', 'Ben Bot', 'Botswana']   |


| returncode          | Description                             |
|---------------------|-----------------------------------------|
| SummaryFound        | A summary hs been found from the querry |
| DisambiguationError | The query match more than ony one page. |
| PageError           | No Wikipedia matched a query            |

## Synapses example

This synapse will look for the {{ query }} spelt by the user on Wikipedia
```
- name: "wikipedia-search"
    neurons:
      - wikipedia:
          language: "en"
          args:
            - query
          file_template: "wikipedia_returned_value.j2"
    signals:
      - order: "look on wikipedia {{ query }}"
```

## Templates example 

This template will simply make Kalliope speak out loud the summary section of the Wikipédia page of the query.
If the query match more than one page, Kaliope will give the user all matched pages.
If the query doesn't match any page on Wikipedia, kalliope will notify the user.
```
{% if returncode == "DisambiguationError" %}
    The query match following pages    
    {% if may_refer is not none %}
        {% for page in may_refer %}
            {{ page }}
        {% endfor %}
    {% endif %}
{% elif returncode == "PageError" %}
    I haven't  found anything on this
{% else %}
    {{ summary }}
{% endif %}
```

## Notes

Complete list of available languages:

- aa
- ab
- ace
- ady
- ady-cyrl
- aeb
- aeb-arab
- aeb-latn
- af
- ak
- aln
- als
- am
- an
- ang
- anp
- ar
- arc
- arn
- arq
- ary
- arz
- as
- ase
- ast
- av
- avk
- awa
- ay
- az
- azb
- ba
- ban
- bar
- bat-smg
- bbc
- bbc-latn
- bcc
- bcl
- be
- be-tarask
- be-x-old
- bg
- bgn
- bh
- bho
- bi
- bjn
- bm
- bn
- bo
- bpy
- bqi
- br
- brh
- bs
- bto
- bug
- bxr
- ca
- cbk-zam
- cdo
- ce
- ceb
- ch
- cho
- chr
- chy
- ckb
- co
- cps
- cr
- crh
- crh-cyrl
- crh-latn
- cs
- csb
- cu
- cv
- cy
- da
- de
- de-at
- de-ch
- de-formal
- diq
- dsb
- dtp
- dty
- dv
- dz
- ee
- egl
- el
- eml
- en
- en-ca
- en-gb
- eo
- es
- et
- eu
- ext
- fa
- ff
- fi
- fit
- fiu-vro
- fj
- fo
- fr
- frc
- frp
- frr
- fur
- fy
- ga
- gag
- gan
- gan-hans
- gan-hant
- gd
- gl
- glk
- gn
- gom
- gom-deva
- gom-latn
- got
- grc
- gsw
- gu
- gv
- ha
- hak
- haw
- he
- hi
- hif
- hif-latn
- hil
- ho
- hr
- hrx
- hsb
- ht
- hu
- hy
- hz
- ia
- id
- ie
- ig
- ii
- ik
- ike-cans
- ike-latn
- ilo
- inh
- io
- is
- it
- iu
- ja
- jam
- jbo
- jut
- jv
- ka
- kaa
- kab
- kbd
- kbd-cyrl
- kg
- khw
- ki
- kiu
- kj
- kk
- kk-arab
- kk-cn
- kk-cyrl
- kk-kz
- kk-latn
- kk-tr
- kl
- km
- kn
- ko
- ko-kp
- koi
- kr
- krc
- kri
- krj
- ks
- ks-arab
- ks-deva
- ksh
- ku
- ku-arab
- ku-latn
- kv
- kw
- ky
- la
- lad
- lb
- lbe
- lez
- lfn
- lg
- li
- lij
- liv
- lki
- lmo
- ln
- lo
- loz
- lrc
- lt
- ltg
- lus
- luz
- lv
- lzh
- lzz
- mai
- map-bms
- mdf
- mg
- mh
- mhr
- mi
- min
- mk
- ml
- mn
- mo
- mr
- mrj
- ms
- mt
- mus
- mwl
- my
- myv
- mzn
- na
- nah
- nan
- nap
- nb
- nds
- nds-nl
- ne
- new
- ng
- niu
- nl
- nl-informal
- nn
- no
- nov
- nrm
- nso
- nv
- ny
- oc
- olo
- om
- or
- os
- pa
- pag
- pam
- pap
- pcd
- pdc
- pdt
- pfl
- pi
- pih
- pl
- pms
- pnb
- pnt
- prg
- ps
- pt
- pt-br
- qu
- qug
- rgn
- rif
- rm
- rmy
- rn
- ro
- roa-rup
- roa-tara
- ru
- rue
- rup
- ruq
- ruq-cyrl
- ruq-latn
- rw
- sa
- sah
- sat
- sc
- scn
- sco
- sd
- sdc
- sdh
- se
- sei
- ses
- sg
- sgs
- sh
- shi
- shi-latn
- shi-tfng
- shn
- si
- simple
- sk
- sl
- sli
- sm
- sma
- sn
- so
- sq
- sr
- sr-ec
- sr-el
- srn
- ss
- st
- stq
- su
- sv
- sw
- szl
- ta
- tcy
- te
- tet
- tg
- tg-cyrl
- tg-latn
- th
- ti
- tk
- tl
- tly
- tn
- to
- tokipona
- tpi
- tr
- tru
- ts
- tt
- tt-cyrl
- tt-latn
- tum
- tw
- ty
- tyv
- tzm
- udm
- ug
- ug-arab
- ug-latn
- uk
- ur
- uz
- uz-cyrl
- uz-latn
- ve
- vec
- vep
- vi
- vls
- vmf
- vo
- vot
- vro
- wa
- war
- wo
- wuu
- xal
- xh
- xmf
- yi
- yo
- yue
- za
- zea
- zh
- zh-classical
- zh-cn
- zh-hans
- zh-hant
- zh-hk
- zh-min-nan
- zh-mo
- zh-my
- zh-sg
- zh-tw
- zh-yue
- zu
