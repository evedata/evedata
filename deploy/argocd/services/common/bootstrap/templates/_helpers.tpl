{{/*
Expand the name of the chart.
*/}}
{{- define "bootstrap.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "bootstrap.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "bootstrap.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels - following Kubernetes recommended labels
https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/
*/}}
{{- define "bootstrap.labels" -}}
helm.sh/chart: {{ include "bootstrap.chart" . }}
{{ include "bootstrap.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: cluster-services
{{- end }}

{{/*
Selector labels
*/}}
{{- define "bootstrap.selectorLabels" -}}
app.kubernetes.io/name: {{ include "bootstrap.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Generate the sync policy for an application
*/}}
{{- define "bootstrap.syncPolicy" -}}
syncPolicy:
  {{- if .automated }}
  automated:
    selfHeal: {{ .automated.selfHeal | default true }}
    prune: {{ .automated.prune | default true }}
  {{- end }}
  syncOptions:
  {{- range .syncOptions }}
    - {{ . }}
  {{- end }}
  {{- if .retry }}
  retry:
    limit: {{ .retry.limit | default 5 }}
    backoff:
      duration: {{ .retry.backoff.duration | default "5s" }}
      factor: {{ .retry.backoff.factor | default 2 }}
      maxDuration: {{ .retry.backoff.maxDuration | default "3m" }}
  {{- end }}
{{- end }}
