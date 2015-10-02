import sublime_plugin
import sublime
import subprocess


class CallPanprocCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # run my external build script that calls pandoc and sed
        # Right now this doesn't handle bibliography entries, nor
        # does it do any processing of stdout or stderr

        settings = sublime.load_settings("Panproc.sublime-settings")
        sh_path = settings.get('sh_path', [])
        panproc_path = settings.get('panproc_path', [])
        file_in = self.view.file_name().replace('\\', '/').replace('C:', '/c')

        # Prepend shell command if provided in settings (needed under windows, not linux):
        if sh_path:
            cmd_str = [sh_path]
            cmd_str.append('--login')
            cmd_str.append('-c')
        else:
            cmd_str = []
        cmd_str.append(panproc_path + ' ' + file_in)

        p = subprocess.Popen(cmd_str, shell='TRUE', stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if p[0].decode(encoding='UTF-8'):
            print('STDOUT: ' + p[0].decode(encoding='UTF-8'))
        if p[1].decode(encoding='UTF-8'):
            print('STDERR: ' + p[1].decode(encoding='UTF-8'))
        return
