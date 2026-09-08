export function formatPrice(value: string | number): string {
  const num = typeof value === 'string' ? Number(value) : value;
  return num.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}