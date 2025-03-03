# import stat for mkdocs

参考 https://shd101wyy.github.io/markdown-preview-enhanced/#/zh-cn/file-imports

## 使用

### install

```sh
pip install mkdocs-import-stat-plugin
```

### use

```yml
plugins:
  - import-stat
```

## 支持的import 语法有：

- `as`
  
@import "hello.xxx" {as="go"}

- `line_begin` 和 `line_end`

@import "hello.xxx" {line_begin=1, line_end=3}

## 拓展语法

一下测试均在 `material` 主题中测试

- `tab` 用于对整个代码块缩进，这样更好地与 material 的 tabs 兼容

```txt
@import "hello.xxx" {tab}
```

  - 也可直接缩进使用，但markdown-preview-enhanced 插件在vscode中就会有渲染问题

```txt
    @import "hello.xxx" 
```

- `p_dir` 用于指定上级路径

eg:

```sh
.
├── docs
│   ├── code
│   │   └── test.html
│   ├── test_dir
│   │   └── test.md
```

test.md

```md
# test

@import "../code/test.html"
```

mkdocs 插件获取当前路径只会获取到 docs 层，最终导致找不到文件

所以可以使用以下方式解决

```md
# test

@import "../code/test.html" {p_dir="test_dir"}
```

## 清空flag

如直接用

````txt
```js {cmd a=x c=x e}
console.log('mkdocs')
```
````

后 mkdocs 渲染会出错，该插件会将其 {cmd a=x c=x e} 删除，这样就与markdown-preview-enhanced 插件不冲突了

## abs_path

指示是否为绝对路径

```md
# test
以下会搜索 系统下的 `/data/test.md` 文件
@import "/data/test.md" {abs_path} 

以下会搜索 当前项目目录下的 `docs/data/test.md` 文件
@import "/data/test.md"
```

## License

[MIT](https://github.com/q9090960bnb3/import-stat-mkdocs-plugin/blob/main/LICENSE)