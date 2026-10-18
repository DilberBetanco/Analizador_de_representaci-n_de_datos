from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        if 'form_numero' in request.POST:
            request.session.pop('error_num', None)
            request.session.pop('resultado_num', None)
            
            numero_str = request.POST.get('numero', '').strip()
            base_str = request.POST.get('base', '10')

            if not numero_str:
                request.session['error_num'] = "Entrada vacía. Por favor, ingrese un número."
            elif numero_str.startswith('-'):
                request.session['error_num'] = "Error: No se permiten valores negativos."
            else:
                try:
                    base = int(base_str)
                    valor_decimal = int(numero_str, base)

                    if not (0 <= valor_decimal <= 65535):
                        request.session['error_num'] = "Error: El valor debe estar entre 0 y 65,535."
                    else:
                        binario_bruto = bin(valor_decimal)[2:]
                        bits_significativos = len(binario_bruto) if valor_decimal > 0 else 1
                        bytes_necesarios = (bits_significativos + 7) // 8 if valor_decimal > 0 else 1
                        bits_completos = bytes_necesarios * 8
                        
                        request.session['resultado_num'] = {
                            'decimal': valor_decimal,
                            'binario': binario_bruto.zfill(bits_completos),
                            'octal': oct(valor_decimal)[2:],
                            'hexadecimal': hex(valor_decimal)[2:].upper(),
                            'bits': bits_significativos,
                            'bytes': bytes_necesarios
                        }
                except ValueError:
                    request.session['error_num'] = f"Error: Dígitos inválidos para la base {base}."

        elif 'form_texto' in request.POST:
            # Limpiamos resultados anteriores de texto
            request.session.pop('error_texto', None)
            request.session.pop('resultado_texto', None)
            
            texto = request.POST.get('texto', '')
            if not texto:
                request.session['error_texto'] = "Entrada vacía. Ingrese un texto."
            elif len(texto) > 20:
                request.session['error_texto'] = "Error: El texto no puede superar los 20 caracteres."
            else:
                analisis = []
                for c in texto:
                    bytes_utf8 = " ".join([hex(b) for b in c.encode('utf-8')])
                    analisis.append({
                        'caracter': c,
                        'decimal': ord(c),
                        'u_hex': f"U+{ord(c):04X}",
                        'hexadecimal': hex(ord(c)),
                        'utf8_bytes': bytes_utf8
                    })
                request.session['resultado_texto'] = analisis

    context = {
        'error_num': request.session.get('error_num'),
        'resultado_num': request.session.get('resultado_num'),
        'error_texto': request.session.get('error_texto'),
        'resultado_texto': request.session.get('resultado_texto'),
    }

    return render(request, 'conversor/index.html', context)