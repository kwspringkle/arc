# Arc

1. [English](#English)
2. [日本語](#日本語)

## English

### Prerequisites

1. **Git Installed**: Ensure you have Git installed on your computer.
2. **GitHub Account**: Make sure you have a GitHub account.

### Steps

#### 1. Fork the repository

1. Go to the [repository](https://github.com/kwspringkle/arc.git) you want to contribute to.
2. Click on the "Fork" button in the upper right corner. This will create a copy of the repository under your GitHub account.

#### 2. Clone Your Fork

1. **Clone the forked repository to your local machine:**
```sh
git clone your-cloned-repo-link
```
2. **Navigate into the cloned repository:**
```sh
cd arc
```
#### 3. Set up the original repository as a remote
Add the original repository as a remote named 'upstream': 
```sh
   git remote add upstream https://github.com/kwspringkle/arc.git
```
Verify the new remote 'upstream':
```sh
git remote -v
```

#### 4. Make changes and commit
```sh
git add .
git commit -m "Description"
```
#### 5. Sync with the original repository
Fetch the latest changes:
```sh
git fetch upstream
```
Merge the latest changes to your branch:
```sh
git merge upstream/main
```
#### 6. Push your changes
Push your changes to the forked repository:
```sh
git push origin your-branch
```
#### 7. Pull Request
After commit to your forked repository, create a pull request. Once your pull request is approved, it will be merged into the main branch of the original repository

## 日本語

### 前提条件

1. **Gitのインストール**: コンピュータにGitがインストールされていることを確認してください。
2. **GitHubアカウント**: GitHubアカウントを持っていることを確認してください。

### 手順

#### 1. リポジトリをフォークする

1. 貢献したい[リポジトリ](https://github.com/kwspringkle/arc.git)に移動します。
2. 右上隅にある「Fork」ボタンをクリックします。これにより、あなたのGitHubアカウント下にリポジトリのコピーが作成されます。

#### 2. フォークをクローンする

1. **フォークしたリポジトリをローカルマシンにクローンします：**
```sh
git clone your-cloned-repo-link
```

2. **クローンしたリポジトリに移動します：**
```sh
cd arc
```

#### 3. 元のリポジトリをリモートとして設定する
元のリポジトリを'upstream'という名前のリモートとして追加します：
```sh
git remote add upstream https://github.com/kwspringkle/arc.git
```
新しいリモート'upstream'を確認します：
```sh
git remote -v
```
#### 4. 変更を加えてコミットする
 ```sh
 git add .
 git commit -m "Description"
 ```
#### 5. 元のリポジトリと同期する
最新の変更をフェッチします：
 ```sh
 git fetch upstream
 ```    
最新の変更をあなたのブランチにマージします：
```sh
git merge upstream/main
```
#### 6.変更をプッシュする
変更をフォークしたリポジトリにプッシュします：  
```sh
git push origin your-branch
```
#### 7. プルリクエスト
フォークしたリポジトリにコミットした後、プルリクエストを作成します。プルリクエストが承認されると、元のリポジトリのメインブランチにマージされます。