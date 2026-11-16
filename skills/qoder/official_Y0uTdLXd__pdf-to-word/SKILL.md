---
name: pdf-to-word
description: �� PDF �ļ�ת��Ϊ Word �ĵ���.docx��
version: 1.0.0
author: YourName
parameters:
  - name: file
    description: Ҫת���� PDF �ļ���֧���ϴ����ṩ·����
    required: true
    type: file
  - name: output_format
    description: �����ʽ��Ŀǰ��֧�� docx
    required: false
    type: string
    default: docx
---
# PDF ת Word ����

## ����
�����û��ϴ��� PDF �ļ�������ת��Ϊ�ɱ༭�� Word �ĵ���.docx����������ת������ļ���

## ʹ�÷�ʽ
1. �û��������з��� PDF �ļ���������ָ�������� PDF ת�� Word�� �� ��������ļ�ת��Ϊ Word ��ʽ����
2. �����Զ����ú�̨�ű�����ת����
3. ת����ɺ󣬷��� Word �ļ����������ӻ�ֱ�����ļ���ʽ���͸��û���

## ע������
- ��Ҫ Python ����������װ `pdf2docx` �⡣
- ת������ PDF ������Ҫ�����ӣ������ĵȴ���
- ��� PDF �������ӱ����ɨ��ͼƬ��ת��Ч���������ޣ�������� OCR ����ʹ�ã���

## ʾ��
�û���`��������ͬ PDF ת�� Word �ļ�`�����ϴ��ļ���
AI�����ü��� �� ����ת����� Word �ļ���