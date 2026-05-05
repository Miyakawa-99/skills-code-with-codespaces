export type Park = {
  id: string
  name: string
}

// 都立公園のテニスコート設置施設（スポレクシステム対象）。
// id は予約システム内部の施設コード。実際の値は wrangler dev でサイトを観察して
// 上書きしてください（README の「公園IDの取り方」参照）。
// 名前は固定で OK。
export const PARKS: Park[] = [
  { id: 'TODO_ARIAKE', name: '有明テニスの森公園' },
  { id: 'TODO_KOMAZAWA', name: '駒沢オリンピック公園' },
  { id: 'TODO_KIBA', name: '木場公園' },
  { id: 'TODO_HIGASHIFUSHIMI', name: '東伏見公園' },
  { id: 'TODO_KOGANEI', name: '小金井公園' },
  { id: 'TODO_HIKARIGAOKA', name: '光が丘公園' },
  { id: 'TODO_MUSASHINO_CHUO', name: '武蔵野中央公園' },
  { id: 'TODO_TONERI', name: '舎人公園' },
  { id: 'TODO_SHINOZAKI', name: '篠崎公園' },
  { id: 'TODO_OI', name: '大井ふ頭中央海浜公園' },
  { id: 'TODO_TATSUMI', name: '辰巳の森海浜公園' },
  { id: 'TODO_WAKASU', name: '若洲海浜公園' },
  { id: 'TODO_RINKAI', name: '臨海町公園' },
]
